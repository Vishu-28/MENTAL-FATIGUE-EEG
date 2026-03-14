def drift_score(timeline):

    transitions = 0

    for i in range(1,len(timeline)):

        if timeline[i] != timeline[i-1]:

            transitions += 1

    return transitions