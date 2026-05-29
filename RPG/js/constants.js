// constants.js

const TILE_SIZE = 32;
const MAP_COLS = 80;
const MAP_ROWS = 80;
const COLLISION_RADIUS = 12;
const SAFE_MARGIN = 2;

const PlayerState = {
    IDLE: 0, WALK: 1, ATTACK: 2, DASH: 3, HURT: 4, DIALOGUE: 5
};

const keys = {};

let canvas, ctx;
let currentSceneId = 'city';
let currentScene;
let map = [];
let camera = { x: 0, y: 0 };
let dialogueState = { active: false, lines: [], lineIdx: 0, charIdx: 0, timer: 0 };
let isPaused = false;

// 画像の読み込み（ダミー画像やプレースホルダーでもエラーにならないようにする）
const images = {
    guild: new Image(), shop: new Image(), forge: new Image(),
    playerAres: new Image(), playerCyan: new Image(), playerLilith: new Image(),
    slime: new Image(), bat: new Image(), skeleton: new Image(), boss: new Image()
};
// 今回は動的デザインのためにCanvas描画をリッチにすることもできるが、仕様書の要件としては画像アセットの読み込みがあった。
// しかしURLがないため、とりあえずオブジェクトだけ用意。

// ソウル・ドライブ（クラス）定義
const souls = {
    'Ares': { name: '剣士アレス', img: 'img/ares.png', maxHp: 150, maxMp: 50, atk: 15, def: 10, spd: 140, level: 1, xp: 0, xpNeeded: 100, color: '#fca5a5' },
    'Cyan': { name: '盗賊シアン', img: 'img/cyan.png', maxHp: 100, maxMp: 80, atk: 12, def: 5, spd: 180, level: 1, xp: 0, xpNeeded: 100, color: '#93c5fd' },
    'Lilith': { name: '魔法使いリリス', img: 'img/lilith.png', maxHp: 80, maxMp: 150, atk: 20, def: 3, spd: 130, level: 1, xp: 0, xpNeeded: 100, color: '#c4b5fd' }
};

// プレイヤー
const player = {
    x: 0, y: 0, vx: 0, vy: 0, spd: 140, radius: 12,
    state: PlayerState.IDLE, angle: 0, attackTimer: 0, dashTimer: 0, dashCd: 0,
    currentSoulId: 'Ares',
    hp: 150, maxHp: 150, mp: 50, maxMp: 50, atk: 15, def: 10,
    level: 1, xp: 0, xpNeeded: 100, gold: 0, weaponLevel: 1, armorLevel: 1,
    inventory: { 'スライムの粘液': 0, '鉄くず': 0, '風の結晶': 0, 'アビスコア': 0, '魔物の肉': 0, '地下野菜': 0 },
    hasBossKey: false,
    activeQuest: null, questProgress: 0,
    warping: false,
    foodBuffs: { maxHp: 0, atk: 0, def: 0, spd: 0 },
    memoryShards: 0, memoryBonuses: { maxHp: 0, crit: 0 },
    skills: {
        I: { name: 'ダッシュ/回避', cd: 0, maxCd: 2, mp: 5 },
        O: { name: '回転斬り/双剣乱舞', cd: 0, maxCd: 5, mp: 10 },
        K: { name: '挑発/トラップ', cd: 0, maxCd: 8, mp: 15 },
        L: { name: '大地の怒り/メテオ', cd: 0, maxCd: 20, mp: 30 }
    }
};

let enemies = [];
let enemyProjectiles = [];
let swordSlashes = [];
let damageParticles = [];
let pushBlocks = [];
let bossCrystals = [];
let chests = [];
let npcs = [];
