from functools import cache

from fabric.utils import clamp


@cache
def lerp(start: float, end: float, progress: float) -> float:
    return start + (end - start) * progress


@cache
def steps(n: int, progress: float, start_jump: bool = False) -> float:
    if start_jump:
        return min(int(progress * n), n - 1) / (n - 1) if n > 1 else 0.0
    return min(int(progress * n + 1e-10), n) / n


@cache
def cubic_bezier(
    x1: float, y1: float, x2: float, y2: float, progress: float, epsilon=1e-6
) -> float:
    # implementation yanked off of the internet, don't blame me about anything.

    if progress <= 0.0 or progress >= 1.0:
        return clamp(progress, 0.0, 1.0)

    t_guess = progress
    for _ in range(8):
        t = t_guess
        t_sq = t * t
        omt = 1.0 - t
        omt_sq = omt * omt

        x = 3 * x1 * omt_sq * t + 3 * x2 * omt * t_sq + t * t_sq
        dx = 3 * x1 * omt_sq + 6 * (x2 - x1) * omt * t + 3 * (1 - x2) * t_sq

        if abs(dx) < epsilon:
            break

        delta = (x - progress) / dx
        t_guess -= delta
        t_guess = clamp(t_guess, 0.0, 1.0)

        if abs(delta) < epsilon:
            break

    t = clamp(t_guess, 0.0, 1.0)
    t_sq = t * t
    omt = 1.0 - t
    return 3 * y1 * omt * omt * t + 3 * y2 * omt * t_sq + t * t_sq


def ease_linear(progress: float) -> float:
    return cubic_bezier(1, 1, 0, 0, progress)


def ease_in(progress: float) -> float:
    return cubic_bezier(0.4, 0, 1, 1, progress)


def ease_out(progress: float) -> float:
    return cubic_bezier(0, 0, 0.2, 1, progress)


def ease_in_out(progress: float) -> float:
    return cubic_bezier(0.4, 0, 0.2, 1, progress)
