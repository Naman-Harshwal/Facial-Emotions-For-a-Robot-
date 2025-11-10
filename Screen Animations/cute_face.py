from manim import *

class CuteFace(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Eyes
        left_eye = Circle(radius=1, color=WHITE, fill_opacity=1).move_to(LEFT * 3 + UP)
        right_eye = Circle(radius=1, color=WHITE, fill_opacity=1).move_to(RIGHT * 3 + UP)

        left_pupil = Circle(radius=0.4, color=BLACK, fill_opacity=1).move_to(left_eye.get_center())
        right_pupil = Circle(radius=0.4, color=BLACK, fill_opacity=1).move_to(right_eye.get_center())

        left_highlight = Circle(radius=0.15, color=WHITE, fill_opacity=1).move_to(left_pupil.get_center() + UP * 0.2 + LEFT * 0.1)
        right_highlight = Circle(radius=0.15, color=WHITE, fill_opacity=1).move_to(right_pupil.get_center() + UP * 0.2 + LEFT * 0.1)

        # Curved Eyelashes (12 o'clock position)
        def create_eyelashes(center):
            lashes = VGroup()
            for angle in [-30, -15, 0, 15, 30]:
                lash = Line(start=ORIGIN, end=UP * 0.4, color=WHITE)
                lash.rotate(angle * DEGREES)
                lash.move_to(center + UP * 1.0)
                lashes.add(lash)
            return lashes

        left_lashes = create_eyelashes(left_eye.get_center())
        right_lashes = create_eyelashes(right_eye.get_center())

        # Mouth (custom curved shape like image)
        mouth_back = ArcBetweenPoints(
            start=LEFT * 2.2 + DOWN * 2.5,
            end=RIGHT * 2.2 + DOWN * 2.5,
            angle=PI/2,
            color=WHITE,
            stroke_width=12
        )
        
        # Dimple effect
        dimple_left = Dot(point=LEFT * 2.5 + DOWN * 2.5, radius=0.08, color=WHITE)
        dimple_right = Dot(point=RIGHT * 2.5 + DOWN * 2.5, radius=0.08, color=WHITE)

        mouth_group = VGroup(mouth_back, dimple_left, dimple_right)

        # Sparkles
        sparkle1 = Star(n=5, fill_opacity=1, color=YELLOW).scale(0.3).move_to(LEFT * 5 + DOWN * 1)
        sparkle2 = Star(n=5, fill_opacity=1, color=YELLOW).scale(0.3).move_to(RIGHT * 5 + DOWN * 1)

        face = VGroup(left_eye, right_eye, left_pupil, right_pupil,
                      left_highlight, right_highlight, left_lashes, right_lashes,
                      mouth_group, sparkle1, sparkle2)

        self.play(FadeIn(face))
        self.wait(1)

        # Eye blink animation
        def blink():
            lid = Rectangle(height=2, width=2, color=BLACK, fill_opacity=1)
            lid_left = lid.copy().move_to(left_eye.get_center())
            lid_right = lid.copy().move_to(right_eye.get_center())
            return Succession(
                AnimationGroup(FadeIn(lid_left), FadeIn(lid_right), lag_ratio=0.1),
                Wait(0.2),
                AnimationGroup(FadeOut(lid_left), FadeOut(lid_right), lag_ratio=0.1),
            )

        self.play(blink())
        self.wait(1)

        self.play(Wiggle(face, scale_value=1.01, rotation_angle=0.01))
        self.wait(2)
