from fabric.widgets.scale import Scale

from ..animator import Animator


class AnimatedScale(Scale):
    """A widget to display a scale with animated transitions."""

    def __init__(self, curve=(0.34, 1.56, 0.64, 1.0), duration=0.8, **kwargs):
        super().__init__(name="animated_scale", **kwargs)
        self.animator = (
            (
                Animator(
                    bezier_curve=curve,
                    duration=duration,
                    min_value=self.min_value,
                    max_value=self.value,
                    tick_widget=self,
                    notify_value=self.set_notify_value,
                )
            )
            .build()
            .play()
            .unwrap()
        )

    def set_notify_value(self, p, *_):
        self.set_value(p.value)

    def animate_value(self, value: float):
        self.animator.pause()
        self.animator.min_value = self.value
        self.animator.max_value = value
        self.animator.play()
        return
