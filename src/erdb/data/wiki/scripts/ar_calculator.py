from copy import copy
from functools import partial
from math import floor
from typing import Any, Iterable, NamedTuple
from js import document, armaments_raw, reinforcements_raw, correction_attack_raw, correction_graph_raw # type: ignore
from pyodide.ffi.wrappers import add_event_listener # type: ignore
from attack_power import CalculatorData, ArmamentCalculator, Attributes # type: ignore

# element is inherit to py-script runtime, assume it's been defined
Element = Element # type: ignore

# instantiating lots of data in JavaScript then porting seems more stable
armaments = armaments_raw.to_py()
reinforcements = reinforcements_raw.to_py()
correction_attack = correction_attack_raw.to_py()
correction_graph = correction_graph_raw.to_py()

calculator_data = CalculatorData(armaments, reinforcements, correction_attack, correction_graph)

active_class = "uk-button-primary"
categories = {a["category"] for a in armaments.values()}

def _to_key(value: str) -> str:
    return value.lower().replace("'", "").replace(".", "").replace(" ", "-")

def _add_click_listener(id: str, callback):
    elem = document.getElementById(id)
    add_event_listener(elem, "click", partial(callback, element=elem))

def _add_click_listeners(format: str, values: Iterable, callback):
    for val in values:
        _add_click_listener(format.format(val), callback)

def _scaling_grade(value: float, null_value: str = "-") -> str:
    if value >= 1.75: return "S"
    if value >= 1.4: return "A"
    if value >= 0.9: return "B"
    if value >= 0.6: return "C"
    if value >= 0.25: return "D"
    if value > 0.0: return "E"
    return null_value

class _AttributeMenu:
    _callback = None
    _attribs = [
        document.getElementById("player-attributes-strength"),
        document.getElementById("player-attributes-dexterity"),
        document.getElementById("player-attributes-intelligence"),
        document.getElementById("player-attributes-faith"),
        document.getElementById("player-attributes-arcane"),
    ]

    def register_callback(self, callback) -> Attributes:
        assert self._callback is None
        self._callback = callback

        for elem in self._attribs:
            add_event_listener(elem, "input", partial(self._on_change, element=elem))

        return self._create_attribs()

    def _create_attribs(self):
        return Attributes(*(int(elem.value) for elem in self._attribs))

    def _on_change(self, *args, element):
        try:
            value = max(1, min(99, int(element.value)))

        except ValueError:
            return

        element.value = value
        self._callback(self._create_attribs()) # type: ignore (optimization to not assert)

class _ArmamentEntry(NamedTuple):
    key: str
    wrapped: Element
    title: Any
    icon: Any
    affinities: Any
    levels: Any
    requirement: dict[str, Any]
    scaling: dict[str, Any]
    attack_power: dict[str, Any]
    status_effect: dict[str, Any]
    guard: dict[str, Any]
    resistance: dict[str, Any]

    @property
    def inner_element(self):
        return self.wrapped.element

    def add_listener(self, template_id_part: str, event: str, callback):
        add_event_listener(self.wrapped.select(f"#armament-display-{template_id_part}").element, event, partial(callback, et=self))

    @classmethod
    def create(cls, key: str, wrapped: Element):
        def get(template_id_part: str):
            return wrapped.select(f"#armament-display-{template_id_part}").element

        return cls(key, wrapped,
            title=get("title"),
            icon=get("icon"),
            affinities=get("affinities"),
            levels=get("levels"),
            requirement={
                "strength": get("requirement-strength"),
                "dexterity": get("requirement-dexterity"),
                "intelligence": get("requirement-intelligence"),
                "faith": get("requirement-faith"),
                "arcane": get("requirement-arcane"),
            },
            scaling={
                "strength": get("scaling-strength"),
                "dexterity": get("scaling-dexterity"),
                "intelligence": get("scaling-intelligence"),
                "faith": get("scaling-faith"),
                "arcane": get("scaling-arcane"),
            },
            attack_power={
                "total": get("attack-power-total"),
                "physical": get("attack-power-physical"),
                "magic": get("attack-power-magic"),
                "fire": get("attack-power-fire"),
                "lightning": get("attack-power-lightning"),
                "holy": get("attack-power-holy"),
            },
            status_effect={
                "bleed": get("status-effect-bleed"),
                "frostbite": get("status-effect-frostbite"),
                "poison": get("status-effect-poison"),
                "scarlet_rot": get("status-effect-scarlet_rot"),
                "sleep": get("status-effect-sleep"),
                "madness": get("status-effect-madness"),
            },
            guard={
                "boost": get("guard-boost"),
                "physical": get("guard-physical"),
                "magic": get("guard-magic"),
                "fire": get("guard-fire"),
                "lightning": get("guard-lightning"),
                "holy": get("guard-holy"),
            },
            resistance={
                "bleed": get("resistance-bleed"),
                "frostbite": get("resistance-frostbite"),
                "poison": get("resistance-poison"),
                "scarlet_rot": get("resistance-scarlet_rot"),
                "sleep": get("resistance-sleep"),
                "madness": get("resistance-madness"),
            },
        )

class _EntryFactory(NamedTuple):
    template = Element("armament-display-template").select("#armament-display-element", from_content=True)

    @staticmethod
    def _icon(armament, profile: str = "icon") -> str:
        return f"https://assets.erdb.workers.dev/icons/armaments/{armament['icon']}/{profile}"

    def create(self, key: str, on_remove) -> _ArmamentEntry:
        armament = armaments[key]
        et = _ArmamentEntry.create(key, self.template.clone())

        et.title.innerText = armament["name"]
        et.icon.src = self._icon(armament, "menu")

        if len(armament["affinity"]) > 1:
            sorted_affinities = [k for k, _ in sorted(armament["affinity"].items(), key=lambda x: x[1]["id"])]
            et.affinities.innerHTML = "<option>" + "</option><option>".join(sorted_affinities) + "</option>"
        else:
            is_somber = armament["upgrade_material"].startswith("Somber")
            et.affinities.innerHTML = f"<option>{'Somber' if is_somber else 'Standard'}</option>"
            et.affinities.disabled = True

        levels = [f"+{i}" for i in range(0, len(armament["upgrade_costs"]) + 1)]
        et.levels.innerHTML = "<option>" + "</option><option>".join(levels) + "</option>"

        et.add_listener("remove", "click", on_remove)

        return et

class _Container:
    _container = Element("armament-display-container").element
    _attribs: Attributes = None
    _calcs: dict[str, ArmamentCalculator] = {}
    _elems: dict[str, _ArmamentEntry] = {}

    def __init__(self, attribute_menu: _AttributeMenu) -> None:
        self._attribs = attribute_menu.register_callback(self._on_attributes)

    @staticmethod
    def _update_values(et: _ArmamentEntry, calc: ArmamentCalculator, attribs: Attributes):
        def norm(val: int) -> str:
            return "-" if val == 0 else str(val)

        armament = armaments[et.key]
        affinity = armament["affinity"][calc.affinity]
        reinforcement = reinforcements[str(affinity["reinforcement_id"])][calc.level]

        ap = calc.attack_power(attribs)

        et.attack_power["total"].innerText = norm(ap.total)
        et.guard["boost"].innerText = norm(floor(affinity["guard"].get("guard_boost", 0.) * reinforcement["guard"]["guard_boost"]))

        for attack_type, value in ap.items():
            et.attack_power[attack_type].innerText = norm(value.total)
            et.guard[attack_type].innerText = norm(floor(affinity["guard"].get(attack_type, 0.) * reinforcement["guard"][attack_type]))

        for effect_type, value in calc.status_effects(attribs).items():
            et.status_effect[effect_type].innerText = norm(value.total)
            et.resistance[effect_type].innerText = norm(floor(affinity["resistance"].get(effect_type, 0.) * reinforcement["resistance"][effect_type]))

        for attribute in ["strength", "dexterity", "intelligence", "faith", "arcane"]:
            scaling = affinity["scaling"].get(attribute, 0.) * reinforcement["scaling"][attribute]
            requirement = armament["requirements"].get(attribute, 0)
            is_met = getattr(attribs, attribute) >= requirement

            et.scaling[attribute].innerText = _scaling_grade(scaling)
            et.scaling[attribute].setAttribute("uk-tooltip", round(scaling, 2))

            getattr(et.requirement[attribute].classList, "remove" if is_met else "add")("uk-text-danger")
            et.requirement[attribute].innerText = norm(requirement)

    def _on_attributes(self, attribs: Attributes):
        self._attribs = attribs

        for et in self._elems.values():
            self._update_values(et, self._calcs[et.key], self._attribs)

    def _on_affinity(self, *args, et: _ArmamentEntry):
        self._calcs[et.key].set_affinity(et.affinities.value, calculator_data)
        self._update_values(et, self._calcs[et.key], self._attribs)

    def _on_level(self, *args, et: _ArmamentEntry):
        level = int(et.levels.value[1:]) # drop initial "+"
        self._calcs[et.key].set_level(level, calculator_data)
        self._update_values(et, self._calcs[et.key], self._attribs)

    def add(self, et: _ArmamentEntry):
        self._calcs[et.key] = ArmamentCalculator(calculator_data, et.key, "Standard", 0)
        self._elems[et.key] = et

        et.add_listener("affinities", "change", self._on_affinity)
        et.add_listener("levels", "change", self._on_level)

        self._update_values(et, self._calcs[et.key], self._attribs)
        self._container.appendChild(et.inner_element)

    def remove(self, key: str):
        self._container.removeChild(self._elems[key].inner_element)
        del self._calcs[key]
        del self._elems[key]

class _ArmamentSelector:
    class _Armament(NamedTuple):
        element: Element

        @staticmethod
        def has_key(element) -> bool:
            return element.getAttribute("data-armament-key") is not None

        @property
        def is_selected(self) -> bool:
            return active_class in self.element.classList

        @property
        def key(self) -> str:
            return self.element.getAttribute("data-armament-key")

        @property
        def category(self) -> str:
            return self.element.getAttribute("data-armament-category")

        def select(self):
            self.element.classList.add(active_class)

        def deselect(self):
            self.element.classList.remove(active_class)

    _factory: _EntryFactory
    _container: _Container

    _choices: list[_Armament]

    _selection: set[str] = set()
    _temporary: set[str] = set()

    _open_button = document.getElementById("open-armament-selection")
    _save_button = document.getElementById("save-armament-selection")

    def __init__(self, factory: _EntryFactory, container: _Container) -> None:
        _add_click_listeners("selection-category-{}", (_to_key(cat) for cat in categories), self.on_category)
        _add_click_listeners("selection-armament-{}", (_to_key(arm) for arm in armaments), self.on_armament)
        _add_click_listener("open-armament-selection", self.on_open)
        _add_click_listener("save-armament-selection", self.on_save)
        _add_click_listener("close-armament-selection", self.on_close)

        self._factory = factory
        self._container = container

        self._choices = [
            self._Armament(a) for a
            in document.getElementById("armament-selection-grid").getElementsByTagName("a")
            if self._Armament.has_key(a)
        ]

    def _on_remove(self, *args, et: _ArmamentEntry):
        self._container.remove(et.key)
        self._selection.remove(et.key)
        self._update_open_button()

    def _update_open_button(self):
        self._open_button.innerHTML = "Select Armaments..." if len(self._selection) == 0 \
            else "<b>1</b> Armament Selected" if len(self._selection) == 1 \
            else f"<b>{len(self._selection)}</b> Armaments Selected"

    def _update_save_button(self):
        self._save_button.innerHTML = f"Save (<b>{len(self._temporary)}</b>)"

    def on_open(self, *args, element=None):
        self._temporary = copy(self._selection)

        # re-select every choice (there may be leftovers from cancelling)
        for arm in self._choices:
            arm.deselect()

            if arm.key in self._temporary:
                arm.select()

        self._update_save_button()

    def on_save(self, *args, element=None):
        for removed in self._selection.difference(self._temporary):
            self._container.remove(removed)

        for added in self._temporary.difference(self._selection):
            et = self._factory.create(added, self._on_remove)
            self._container.add(et)

        self._selection = copy(self._temporary)
        self.on_close()

    def on_close(self, *args, element=None):
        self._temporary.clear()
        self._update_open_button()

    def on_category(self, *args, element):
        choices = [
            arm for arm in self._choices
            if arm.category == element.getAttribute("data-armament-category")
        ]

        if all(a.is_selected for a in choices):
            [self.on_armament(element=a.element) for a in choices if a.is_selected]

        else:
            [self.on_armament(element=a.element) for a in choices if not a.is_selected]

    def on_armament(self, *args, element):
        arm = self._Armament(element)

        if arm.is_selected:
            self._temporary.remove(arm.key)
            arm.deselect()

        else:
            self._temporary.add(arm.key)
            arm.select()

        self._update_save_button()

factory = _EntryFactory()
attribute_menu = _AttributeMenu()
container = _Container(attribute_menu)

selector = _ArmamentSelector(factory, container)
selector.on_save()