const CODE_TO_NAME = {
  KeyA: 'A', KeyB: 'B', KeyC: 'C', KeyD: 'D', KeyE: 'E', KeyF: 'F', KeyG: 'G',
  KeyH: 'H', KeyI: 'I', KeyJ: 'J', KeyK: 'K', KeyL: 'L', KeyM: 'M', KeyN: 'N',
  KeyO: 'O', KeyP: 'P', KeyQ: 'Q', KeyR: 'R', KeyS: 'S', KeyT: 'T', KeyU: 'U',
  KeyV: 'V', KeyW: 'W', KeyX: 'X', KeyY: 'Y', KeyZ: 'Z',
  Digit0: '0', Digit1: '1', Digit2: '2', Digit3: '3', Digit4: '4',
  Digit5: '5', Digit6: '6', Digit7: '7', Digit8: '8', Digit9: '9',
  Space: 'SPACE', Enter: 'ENTER', Escape: 'ESC', Tab: 'TAB',
  ShiftLeft: 'SHIFT', ShiftRight: 'SHIFT',
  ControlLeft: 'CTRL', ControlRight: 'CTRL',
  AltLeft: 'ALT', AltRight: 'ALT',
  Backspace: 'BACKSPACE',
  ArrowUp: 'UP', ArrowDown: 'DOWN', ArrowLeft: 'LEFT', ArrowRight: 'RIGHT'
};

const IS_MAC = /Mac|iPhone|iPad/.test(navigator.platform || '') || /Mac OS/.test(navigator.userAgent || '');
if (IS_MAC) {
  CODE_TO_NAME.MetaLeft = 'CMD';
  CODE_TO_NAME.MetaRight = 'CMD';
}

const DISPLAY = {
  SPACE: 'Space', ENTER: 'Enter', ESC: 'Esc', TAB: 'Tab', SHIFT: 'Shift',
  CTRL: 'Ctrl', ALT: 'Alt', CMD: 'Cmd', BACKSPACE: 'Bksp',
  UP: 'Up', DOWN: 'Down', LEFT: 'Left', RIGHT: 'Right'
};

const DEFAULT_MAPPING = {
  DPAD_UP: 'W', DPAD_DOWN: 'S', DPAD_LEFT: 'A', DPAD_RIGHT: 'D',
  STICK_UP: 'W', STICK_DOWN: 'S', STICK_LEFT: 'A', STICK_RIGHT: 'D',
  RSTICK_UP: 'T', RSTICK_LEFT: 'J', RSTICK_DOWN: 'K', RSTICK_RIGHT: 'I',
  BUTTON_0: 'J', BUTTON_1: 'K', BUTTON_2: 'I', BUTTON_3: 'T',
  BUTTON_4: 'M', BUTTON_5: 'L', BUTTON_6: 'SPACE', BUTTON_7: 'ENTER',
  BUTTON_8: 'N', BUTTON_9: 'ESC', BUTTON_10: '1', BUTTON_11: '2',
  BUTTON_12: '', BUTTON_13: ''
};

const ICONS = {
  trigger: '<svg viewBox="0 0 24 24"><path d="M5 15c2.5-6 5-8 7-8s4.5 2 7 8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M8 15h8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
  bumper: '<svg viewBox="0 0 24 24"><path d="M4 14c2-5 4.5-6 8-6s6 1 8 6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
  share: '<svg viewBox="0 0 24 24"><path d="M8 12h8M8 8l-3 4 3 4M16 8l3 4-3 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  dpad: '<svg viewBox="0 0 24 24"><path d="M10 4h4v6h6v4h-6v6h-4v-6H4v-4h6V4z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>',
  stick: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="7" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="12" cy="12" r="2.2" fill="currentColor"/></svg>',
  touch: '<svg viewBox="0 0 24 24"><rect x="4" y="7" width="16" height="10" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 15.5h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
  options: '<svg viewBox="0 0 24 24"><path d="M6 8h12M6 12h12M6 16h12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
  press: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M12 8.5v4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
  ps: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M7.5 13.2c1.4-2.4 2.8-3.4 4.5-3.4s3.1 1 4.5 3.4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
};

const PILLS = [
  { id: 'l2', side: 'shoulder-left', label: 'L2', icon: 'trigger', color: '#6ec8ff', keys: ['BUTTON_6'] },
  { id: 'l1', side: 'shoulder-left', label: 'L1', icon: 'bumper', color: '#3d8dff', keys: ['BUTTON_4'] },
  { id: 'share', side: 'left', label: 'Share / Create', icon: 'share', color: '#3ddc97', keys: ['BUTTON_8'] },
  { id: 'dpad', side: 'left', label: 'D-Pad', icon: 'dpad', color: '#e7f08a', keys: ['DPAD_UP', 'DPAD_LEFT', 'DPAD_DOWN', 'DPAD_RIGHT'], titles: ['Up', 'Left', 'Down', 'Right'] },

  { id: 'touch', side: 'top', label: 'Touchpad', icon: 'touch', color: '#49d2ff', keys: ['BUTTON_13'] },

  { id: 'r1', side: 'shoulder-right', label: 'R1', icon: 'bumper', color: '#ff7a45', keys: ['BUTTON_5'] },
  { id: 'r2', side: 'shoulder-right', label: 'R2', icon: 'trigger', color: '#ffb020', keys: ['BUTTON_7'] },
  { id: 'options', side: 'right', label: 'Options / Menu', icon: 'options', color: '#2ee6c7', keys: ['BUTTON_9'] },
  { id: 'triangle', side: 'right', label: 'Triangle', glyph: '△', color: '#5ce1ff', keys: ['BUTTON_3'] },
  { id: 'square', side: 'right', label: 'Square', glyph: '□', color: '#ff5ad5', keys: ['BUTTON_0'] },
  { id: 'circle', side: 'right', label: 'Circle', glyph: '○', color: '#ff4b6e', keys: ['BUTTON_2'] },
  { id: 'cross', side: 'right', label: 'Cross', glyph: '✕', color: '#6aa2ff', keys: ['BUTTON_1'] },

  { id: 'lstick', side: 'center', label: 'Left Stick', icon: 'stick', color: '#c084fc', keys: ['STICK_UP', 'STICK_LEFT', 'STICK_DOWN', 'STICK_RIGHT'], titles: ['Up', 'Left', 'Down', 'Right'] },
  { id: 'l3', side: 'center', label: 'L3', icon: 'press', color: '#8b5cf6', keys: ['BUTTON_10'] },
  { id: 'ps', side: 'center', label: 'PlayStation', icon: 'ps', color: '#f4f7fb', keys: ['BUTTON_12'] },
  { id: 'r3', side: 'center', label: 'R3', icon: 'press', color: '#e879f9', keys: ['BUTTON_11'] },
  { id: 'rstick', side: 'center', label: 'Right Stick', icon: 'stick', color: '#9aa8ff', keys: ['RSTICK_UP', 'RSTICK_LEFT', 'RSTICK_DOWN', 'RSTICK_RIGHT'], titles: ['Up / Triangle', 'Left / Square', 'Down / Cross', 'Right / Circle'] }
];

const BOUND_KEYS = [...new Set(PILLS.flatMap((pill) => pill.keys))];

const FAMILIES = {
  playstation: {
    art: './controllers/playstation.png',
    alt: 'PlayStation controller',
    labels: {
      l2: 'L2', l1: 'L1', share: 'Share / Create', touch: 'Touchpad',
      r1: 'R1', r2: 'R2', options: 'Options / Menu',
      triangle: 'Triangle', square: 'Square', circle: 'Circle', cross: 'Cross',
      ps: 'PlayStation'
    },
    glyphs: { triangle: '△', square: '□', circle: '○', cross: '✕' },
    colors: {},
    hide: []
  },
  xbox: {
    art: './controllers/xbox.png',
    alt: 'Xbox controller',
    labels: {
      l2: 'LT', l1: 'LB', share: 'View',
      r1: 'RB', r2: 'RT', options: 'Menu',
      triangle: 'Y', square: 'X', circle: 'B', cross: 'A',
      ps: 'Xbox'
    },
    glyphs: { triangle: 'Y', square: 'X', circle: 'B', cross: 'A' },
    colors: {
      triangle: '#f5c542', square: '#4aa3ff', circle: '#ff4d4d', cross: '#3ddc6e', ps: '#9be7a4'
    },
    hide: ['touch']
  }
};

let currentMapping = { ...DEFAULT_MAPPING };
let savedSnapshot = JSON.stringify(currentMapping);
let listeningKey = null;
let chordMods = [];
let activeFamily = 'playstation';
const pillNodes = {};

function displayKey(name) {
  if (!name) return '';
  return DISPLAY[name] || name;
}

function displayBinding(value) {
  if (!value) return '';
  return String(value).split('+').map((part) => displayKey(part.trim())).filter(Boolean).join(' + ');
}

function setStatus(text) {
  const note = document.getElementById('status-note');
  note.textContent = text || '';
}

function refreshSavedState() {
  const dirty = JSON.stringify(currentMapping) !== savedSnapshot;
  const el = document.getElementById('save-state');
  el.textContent = dirty ? 'Not saved yet' : 'Saved';
  el.classList.toggle('unsaved', dirty);
}

function buildPills() {
  const columns = {
    left: document.getElementById('col-left'),
    right: document.getElementById('col-right'),
    top: document.getElementById('touch-slot'),
    'shoulder-left': document.getElementById('shoulder-left'),
    'shoulder-right': document.getElementById('shoulder-right'),
    center: document.getElementById('col-center')
  };

  for (const pill of PILLS) {
    const node = document.createElement('div');
    node.className = 'pill';
    node.id = `pill-${pill.id}`;
    node.dataset.side = pill.side;
    node.style.setProperty('--accent', pill.color);

    const icon = document.createElement('span');
    icon.className = 'pill-icon';
    if (pill.glyph) {
      icon.classList.add('glyph');
      icon.textContent = pill.glyph;
    } else {
      icon.innerHTML = ICONS[pill.icon] || '';
    }

    const label = document.createElement('span');
    label.className = 'pill-label';
    label.textContent = pill.label;

    const chips = document.createElement('span');
    chips.className = 'pill-chips';

    if (pill.staticChip) {
      const chip = document.createElement('span');
      chip.className = 'keychip is-static';
      chip.textContent = '—';
      chips.appendChild(chip);
    } else {
      pill.keys.forEach((key, index) => {
        const chip = document.createElement('button');
        chip.type = 'button';
        chip.className = 'keychip';
        chip.dataset.key = key;
        if (pill.titles) chip.title = pill.titles[index];
        chip.addEventListener('click', (event) => onChipClick(event, key));
        chips.appendChild(chip);
      });
    }

    node.append(icon, label, chips);
    columns[pill.side].appendChild(node);
    pillNodes[pill.id] = { pill, node };
  }

  paintChips();
}

function paintChips() {
  for (const { pill } of Object.values(pillNodes)) {
    for (const key of pill.keys) {
      const chip = document.querySelector(`.keychip[data-key="${key}"]`);
      if (!chip) continue;
      const value = displayBinding(currentMapping[key]);
      const listening = listeningKey === key;
      chip.classList.toggle('listening', listening);
      chip.replaceChildren();
      const text = document.createElement('span');
      text.className = 'keychip-value';
      if (listening && chordMods.length) text.textContent = displayBinding(chordMods.join('+')) + ' + …';
      else text.textContent = listening ? '…' : (value || 'Key');
      if (!value && !listening) text.style.opacity = '0.4';
      chip.appendChild(text);
      if (value && !listening) {
        const clear = document.createElement('span');
        clear.className = 'keychip-clear';
        clear.textContent = '×';
        clear.dataset.clear = key;
        chip.appendChild(clear);
      }
    }
  }
}

function onChipClick(event, key) {
  event.stopPropagation();
  if (event.target.closest('.keychip-clear')) {
    currentMapping[key] = '';
    listeningKey = null;
    chordMods = [];
    paintChips();
    refreshSavedState();
    setStatus('');
    return;
  }
  listeningKey = listeningKey === key ? null : key;
  chordMods = [];
  paintChips();
  setStatus(listeningKey ? (IS_MAC
    ? 'Press a key, or hold Command, Ctrl, Alt, or Shift and then a key'
    : 'Press a key, or hold Ctrl, Alt, or Shift and then a key') : '');
}

function finishListen() {
  listeningKey = null;
  chordMods = [];
  paintChips();
  refreshSavedState();
  setStatus('');
}

function heldModifiers(event, name) {
  const mods = [];
  if (IS_MAC && (event.metaKey || name === 'CMD')) mods.push('CMD');
  if (event.ctrlKey || name === 'CTRL') mods.push('CTRL');
  if (event.altKey || name === 'ALT') mods.push('ALT');
  if (event.shiftKey || name === 'SHIFT') mods.push('SHIFT');
  return mods;
}

function assignFromKeyboard(event) {
  if (!listeningKey) return;
  const name = CODE_TO_NAME[event.code];
  if (!name) return;
  event.preventDefault();
  event.stopPropagation();
  if (event.repeat) return;

  const mods = heldModifiers(event, name);
  if (name === 'CMD' || name === 'CTRL' || name === 'ALT' || name === 'SHIFT') {
    chordMods = mods;
    paintChips();
    setStatus(displayBinding(mods.join('+')) + ' + …');
    return;
  }

  currentMapping[listeningKey] = [...mods, name].join('+');
  finishListen();
}

function assignFromKeyUp(event) {
  if (!listeningKey || !chordMods.length) return;
  if (event.ctrlKey || event.altKey || event.shiftKey || (IS_MAC && event.metaKey)) return;
  event.preventDefault();
  currentMapping[listeningKey] = chordMods.join('+');
  finishListen();
}

function applyFamily(family) {
  const next = family === 'xbox' ? 'xbox' : 'playstation';
  if (next === activeFamily) return;
  activeFamily = next;
  const spec = FAMILIES[next];
  const art = document.getElementById('controller-art');
  art.src = spec.art;
  art.alt = spec.alt;

  for (const [id, { pill, node }] of Object.entries(pillNodes)) {
    const label = spec.labels[id];
    if (label) node.querySelector('.pill-label').textContent = label;
    const icon = node.querySelector('.pill-icon');
    const glyph = spec.glyphs[id];
    if (glyph) icon.textContent = glyph;
    if (id === 'ps') icon.innerHTML = next === 'xbox'
      ? '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 8l8 8M16 8l-8 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
      : ICONS.ps;
    const color = spec.colors[id] || pill.color;
    node.style.setProperty('--accent', color);
    node.hidden = spec.hide.includes(id);
  }

  const rightTitles = next === 'xbox'
    ? ['Up / Y', 'Left / X', 'Down / A', 'Right / B']
    : ['Up / Triangle', 'Left / Square', 'Down / Cross', 'Right / Circle'];
  document.querySelectorAll('#pill-rstick .keychip').forEach((chip, index) => {
    chip.title = rightTitles[index];
  });

  const dpad = pillNodes.dpad.node;
  const stick = pillNodes.lstick.node;
  const left = document.getElementById('col-left');
  const center = document.getElementById('col-center');
  if (next === 'xbox') {
    center.prepend(dpad);
    left.appendChild(stick);
  } else {
    center.prepend(stick);
    left.appendChild(dpad);
  }
}

function applyActive(activeInputs) {
  const active = new Set(activeInputs || []);
  for (const { pill, node } of Object.values(pillNodes)) {
    const hit = pill.keys.some((key) => active.has(key));
    node.classList.toggle('active', hit);
    for (const key of pill.keys) {
      const chip = document.querySelector(`.keychip[data-key="${key}"]`);
      if (chip) chip.classList.toggle('active', active.has(key));
    }
  }
}

function setToggle(isActive) {
  document.getElementById('toggle-text').textContent = isActive ? 'Pause' : 'Resume';
  document.getElementById('toggle-icon').textContent = isActive ? 'II' : '▶';
}

async function loadMapping() {
  try {
    const response = await fetch('/api/mapping');
    const data = await response.json();
    currentMapping = { ...DEFAULT_MAPPING, ...data.mapping };
    savedSnapshot = JSON.stringify(currentMapping);
    paintChips();
    refreshSavedState();
  } catch (error) {
    setStatus('Showing default keys');
  }
}

function startPolling() {
  setInterval(async () => {
    try {
      const response = await fetch('/api/state');
      const state = await response.json();
      const device = document.getElementById('device-status');
      const text = document.getElementById('device-text');
      if (state.connected) {
        device.classList.remove('offline');
        text.textContent = state.device_name;
        applyFamily(state.family);
      } else {
        device.classList.add('offline');
        text.textContent = 'Plug in a controller';
        applyFamily('playstation');
      }
      applyActive(state.active_inputs);
      setToggle(state.is_active);
    } catch (error) {
      // The page can still be previewed without the adapter.
    }
  }, 40);
}

async function toggleAdapter() {
  await fetch('/api/toggle', { method: 'POST' });
}

async function saveProfile() {
  const response = await fetch('/api/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(currentMapping)
  });
  if (!response.ok) throw new Error('save failed');
  savedSnapshot = JSON.stringify(currentMapping);
  refreshSavedState();
  setStatus('Profile saved');
}

async function resetDefaults() {
  const response = await fetch('/api/reset', { method: 'POST' });
  const data = await response.json();
  currentMapping = { ...DEFAULT_MAPPING, ...data.mapping };
  savedSnapshot = JSON.stringify(currentMapping);
  finishListen();
  setStatus('Restored defaults');
}

async function clearAll() {
  for (const key of BOUND_KEYS) currentMapping[key] = '';
  chordMods = [];
  listeningKey = null;
  paintChips();
  await saveProfile();
  setStatus('All bindings cleared');
}

function init() {
  buildPills();
  document.getElementById('btn-toggle').addEventListener('click', () => {
    toggleAdapter().catch(() => setStatus('Adapter is not running'));
  });
  document.getElementById('btn-save').addEventListener('click', () => {
    saveProfile().catch(() => setStatus('Could not save'));
  });
  document.getElementById('btn-reset').addEventListener('click', () => {
    resetDefaults().catch(() => setStatus('Could not reset'));
  });
  document.getElementById('btn-clear').addEventListener('click', () => {
    clearAll().catch(() => setStatus('Could not clear'));
  });
  window.addEventListener('keydown', assignFromKeyboard, true);
  window.addEventListener('keyup', assignFromKeyUp, true);
  window.addEventListener('pointerdown', (event) => {
    if (!event.target.closest('.keychip')) {
      if (listeningKey) finishListen();
    }
  });
  loadMapping();
  startPolling();
}

init();
