from lib import USER_INI
from lib.data import (
    PALICO_CLASSES,
    SKILL_DATA,
    SKILL_COMBOS,
    SKILL_COMBOS_CHARISMA,
)


def filter_skills(skill_type, skill_group=None):
    for data in (i for i in SKILL_DATA
                 if i['type'].lower() == skill_type.lower()):
        if skill_group:
            if data['group'].lower() == skill_group.lower():
                yield data
        else:
            yield data


def valid_user_ini(ini=USER_INI):
    # Checks if class is valid
    pal_class = ini['class']
    if pal_class.lower() not in [i.lower() for i in PALICO_CLASSES]:
        return False

    # Checks if support skills are valid
    support = ini['support_skills']
    support_cost = []
    support_cmb = []
    costs = {'a': 3, 'b': 2, 'c': 1}
    for g, s in support.items():
        skills = [i['name'].lower()
                  for i in filter_skills('support', skill_group=g)]

        if not all(True if i.lower() in skills else False for i in s):
            print('Invalid support skill selection: {}'.format({g: s}))
            return False

        cost = costs.get(g.lower(), 0)
        support_cost.extend([cost for _ in s])
        support_cmb.extend([g.upper() for _ in s])

    # Checks if passive skills are valid
    passive = ini['passive_skills']
    passive_cost = []
    passive_cmb = []
    for g, s in passive.items():
        skills = [i['name'].lower()
                  for i in filter_skills('passive', skill_group=g)]

        if not all(True if i.lower() in skills else False for i in s):
            print('Invalid passive skill selection: {}'.format({g: s}))
            return False

        cost = costs.get(g.lower(), 0)
        passive_cost.extend([cost for _ in s])
        passive_cmb.extend([g.upper() for _ in s])

    # Checks if skill combination and cost is valid
    # FIXME: The combination checks is still pretty naive
    max_cost = 9 if pal_class.lower() == 'charisma' else 8
    ok_passive, ok_support = False, False

    if support_cost.count(3) > 1:
        print('You cannot choose more than 1 support skill from the A group!')
        return False

    if passive_cost.count(3) > 1:
        print('You cannot choose more than 1 passive skill from the A group!')
        return False

    combos = (SKILL_COMBOS_CHARISMA if pal_class == 'charisma'
              else SKILL_COMBOS)
    for cmb in combos:
        if sorted(passive_cmb) == sorted(cmb):
            ok_passive = True
        if sorted(support_cmb) == sorted(cmb):
            ok_support = True

    if sum(support_cost) > max_cost:
        print('Total cost of support skill cannot exceed {}'.format(max_cost))
        print('Support combo: {}'.format(support_cost))
        return False

    if sum(support_cost) == max_cost and not ok_support:
        print('Support combo is not valid')
        print('Support combo: {}'.format(support_cost))
        return False

    if sum(passive_cost) > max_cost:
        print('Total cost of passive skill cannot exceed {}'.format(max_cost))
        print('Passive combo: {}'.format(passive_cost))
        return False

    if sum(passive_cost) == max_cost and not ok_passive:
        print('Passive combo is not valid')
        print('Passive combo: {}'.format(passive_cost))
        return False

    return True


def ave_chance(val):
    total = sum(val) / len(val)
    return total * 100


def main():
    passive = USER_INI['passive_skills']
    support = USER_INI['support_skills']
    passive_skills = []
    support_skills = []

    for g, s in support.items():
        _data = filter_skills('support', skill_group=g)
        support_skills.extend([i for i in _data
                               if i['name'].lower() in [x.lower() for x in s]])

    print('Support skills:')
    for n in (i['name'] for i in support_skills):
        print(n)
    print()

    for g, s in passive.items():
        _data = filter_skills('passive', skill_group=g)
        passive_skills.extend([i for i in _data
                               if i['name'].lower() in [x.lower() for x in s]])

    print('Passive skills:')
    for n in (i['name'] for i in passive_skills):
        print(n)
    print()

    selected_skills = passive_skills + support_skills
    out = {}

    for sk in selected_skills:
        chances = {k: v for k, v in sk.items() if '_chance' in k}

        for k, v in chances.items():
            if k not in out:
                out[k] = []
            out[k].append(v)

    out = {k: ave_chance(v) for k, v in out.items()}
    for k, v in sorted([i for i in out.items()], key=lambda x: x[1],
                       reverse=True):
        print('{}: {:.2f}%'.format(k, v))


if __name__ == '__main__':
    if valid_user_ini():
        main()
