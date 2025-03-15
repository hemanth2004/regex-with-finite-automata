from app.app import build_fa

regex = "0(10)*(110)*"
test_string = "0110"

fa = build_fa(
        regex, 
        verbose                          =True, 
        if_remove_duplicate_transitions  =True, 
        if_convert_to_dfa                =True, 
        if_find_shortest_accepting_string=True, 
        if_minimize_dfa                  =True, 
        if_report_stats                  =True)

print("--------------------------------")
print("Regex      :", regex)
print("Test string:", test_string)
print("Result     :", fa.run(test_string))
