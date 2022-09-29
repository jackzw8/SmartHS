from card.basic_card import Coin
from card.standard_card import *
from card.classic_card import *
from card.hero_power_card import *

ID2CARD_DICT = {
    # 特殊项-幸运币
    "COIN": Coin,

    # 英雄技能
    "TOTEMIC_CALL": TotemicCall,  # 萨满  图腾召唤
    "LESSER_HEAL": LesserHeal,  # 牧师  次级治疗术
    "BALLISTA_SHOT": BallistaShot,  # 猎人  稳固射击
    "FIRE_BLAST": FireBlast,  # 法师  火焰冲击
    "SHAPE_SHIFT": ShapeShift,  # 德鲁伊  变形
    "ARMOR_UP": ArmorUp,  # 战士  全副武装！
    "REINFORCE": Reinforce,  # 骑士  援军
    # 术士  生命分流
    # 盗贼  匕首精通

    # 经典模式
    # 中立
    "VAN_CS2_189": ElvenArcher,  # 精灵弓箭手
    "VAN_NEW1_021": DoomSayer,  # 末日预言者
    "VAN_CS2_117": EarthenRingFarseer,  # 大地之环先知
    "VAN_EX1_085": MindControlTech,  # 精神控制技师
    "VAN_EX1_007": AcolyteOfPain,  # 苦痛侍僧
    "VAN_EX1_590": BloodKnight,  # 血骑士
    "VAN_EX1_097": Abomination,  # 憎恶
    "VAN_EX1_284": AzureDrake,  # 碧蓝幼龙
    "VAN_NEW1_041": StampedingKodo,  # 狂奔科多兽

    "VAN_EX1_116": LeeroyJenkins,  # 火车王！！！！！！
    "VAN_EX1_562": Onyxia,  # 奥妮克希亚

    # 萨满
    "VAN_EX1_238": LightingBolt,  # 闪电箭
    "VAN_EX1_247": StormforgedAxe,  # 雷铸战斧
    "VAN_EX1_259": LightningStorm,  # 闪电风暴
    "VAN_EX1_248": FeralSpirit,  # 野性狼魂
    "VAN_EX1_246": Hex,  # 妖术
    "VAN_CS2_042": FireElemental,  # 火元素
    "VAN_EX1_250": EarthElemental,  # 土元素

    # 猎人
    "VAN_EX1_536": EaglehornBow,  # 鹰角弓
    "VAN_EX1_538": UnleashTheHounds,  # 关门放狗
    "VAN_NEW1_031": AnimalCompanion,  # 动物伙伴
    "VAN_EX1_534": Highmane,  # 长鬃草原狮
    "VAN_CS2_203": IronbeakOwl,  # 铁喙猫头鹰

    # 法师
    "VAN_CS2_022": Polymorph,  # 变形术
    "VAN_CS2_033": WaterElemental,  # 水元素
    "VAN_CS2_029": FireBall,  # 火球术
    "VAN_CS2_024": FrostBolt,  # 寒冰箭
    "VAN_CS2_023": ArcaneIntellect,  # 奥术智慧
    "VAN_EX1_277": ArcaneMissiles,  # 奥术飞弹

    # 德鲁伊
    "VAN_EX1_169": Innervate,  # 激活
    "VAN_CS2_012": Swipe,  # 横扫

    # 战士
    "VAN_CS2_106": FieryWarAxe,  # 炽炎战斧
    "VAN_EX1_414": GrommashHellscream,  # 格罗玛什·地狱咆哮

    # 骑士
    "VAN_CS2_097": TruesilverChampion,  # 真银圣剑
    "VAN_EX1_383": TirionFordring,  # 佛丁
    "VAN_CS2_093": Consecration,  # 奉献

    # 标准模式-牧师
    # "BAR_026": DeathsHeadCultist,  # 亡首教徒

    # "YOP_032": ArmorVendor,  # 护甲商贩
    # "CORE_CS1_130": HolySmite,  # 神圣惩击
    # "CS1_130": HolySmite,  # 神圣惩击
    # "SCH_250": WaveOfApathy,  # 倦怠光波
    # "BT_715": BonechewerBrawler,  # 噬骨殴斗者
    # "CORE_EX1_622": ShadowWordDeath,  # 暗言术：灭
    # "EX1_622": ShadowWordDeath,  # 暗言术：灭
    # "BT_257": Apotheosis,  # 神圣化身
    # "BAR_311": DevouringPlague,  # 噬灵疫病
    # "BT_730": OverconfidentOrc,  # 狂傲的兽人
    # "CORE_CS1_112": HolyNova,  # 神圣新星
    # "CS1_112": HolyNova,  # 神圣新星
    # "YOP_006": Hysteria,  # 狂乱
    # "CORE_EX1_197": ShadowWordRuin,  # 暗言术：毁
    # "EX1_197": ShadowWordRuin,  # 暗言术：毁
    # "WC_014": AgainstAllOdds,  # 除奇致胜
    # "BT_720": RuststeedRaider,  # 锈骑劫匪
    # "CS3_024": TaelanFordring,  # 泰兰·弗丁
    # "EX1_110": CairneBloodhoof,  # 凯恩·血蹄
    # "CORE_EX1_110": CairneBloodhoof,  # 凯恩·血蹄
    # "WC_030": MutanusTheDevourer,  # 吞噬者穆坦努斯
    # "BT_198": SoulMirror,  # 灵魂之镜
    # "DMF_053": BloodOfGhuun,  # 戈霍恩之血

}
