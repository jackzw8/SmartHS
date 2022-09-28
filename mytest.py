from strategy_entity import StrategyMinion

def aaa(my_minion,oppo_minion):
    tmp_delta_h = 0
    # 启发值大的要考虑一下。 启发值小的随从就直接送给对方启发值大的随从了，腾格子，打开随从交换的局面。
    if my_minion.heuristic_val > 4 or oppo_minion.heuristic_val < 6:
        tmp_delta_h -= my_minion.delta_h_after_damage(oppo_minion.attack)
    tmp_delta_h += oppo_minion.delta_h_after_damage(my_minion.attack)

    return tmp_delta_h

if __name__ == "__main__":
    mysm1 = StrategyMinion('SW_111','HAND','','1',0,0,2,1)
    mysm2 = StrategyMinion('SW_111','HAND','','2',0,0,3,1)
    mysm3 = StrategyMinion('SW_111','HAND','','5',0,0,7,8)
    opsm1 = StrategyMinion('SW_111','HAND','','5',0,0,4,5)
    opsm2 = StrategyMinion('SW_111','HAND','','5',0,0,4,3)
    print(mysm1.heuristic_val)
    print(mysm2.heuristic_val)
    print(mysm3.heuristic_val)
    print(opsm1.heuristic_val)
    print(opsm2.heuristic_val)

    print(aaa(mysm1,opsm1))
    print(aaa(mysm2,opsm1))
    print(aaa(mysm3,opsm1))
    print(aaa(mysm2,opsm2))
    print(aaa(mysm3,opsm2))
