#Mapping dictionary collector type -- access policy A
policy_mapping = {'A': '((a1 or a2) and (a3 or a4))',
                  'B': '((b1 or b2) and (b3 or b4))',
                  'C': '((c1 or c2) and (c3 or c4))',
                  'D': '((d1 or d2) and (d3 or d4))'}

my_string = "A123"
for key, value in policy_mapping.items():
    if key in my_string.upper():
        print(policy_mapping[key])


