def normalize_vix(vix_value):
    VIX_MIN = 10  # 극저변동성
    VIX_MAX = 80  # 금융위기급 공포
    score = max(0, min(1, (VIX_MAX - vix_value) / (VIX_MAX - VIX_MIN)))
    return score * 100


def normalize_fgi(fgi_value):
    return max(0, min(100, fgi_value))


def calculate_market_score(vix_value: float, fgi_value: float) -> float:
    vix_score = normalize_vix(vix_value)
    fgi_score = normalize_fgi(fgi_value)

    # 가중치: VIX 60%, FGI 40%
    total_score = (vix_score * 0.6) + (fgi_score * 0.4)
    return round(total_score, 2)
