def compute_mfbi(theta, alpha, beta, drift):

    score = (theta + drift)/(alpha + beta + 0.01)

    if score < 0.8:
        return "Low", score

    elif score < 1.5:
        return "Moderate", score

    else:
        return "High", score