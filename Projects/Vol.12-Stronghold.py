from manimlib import *


# 该函数来自Manim Kindergarten Sandbox
def debug(self, tex, scale_factor=0.6, text_color=PURPLE):
    for i, j in enumerate(tex):
        tex_id = Text(str(i), font="Consolas").scale(scale_factor).set_color(text_color)
        tex_id.move_to(j)
        self.add(tex_id)


# 感谢乐正垂星指导该函数的设计
def arc_text(text, radius, angle, arc_buff):
    nums = len(text)
    for i in range(nums):
        text[i].move_to(radius * UP).rotate(- i * (angle / (nums - 1)) * DEGREES, about_point=ORIGIN)
    text.rotate((angle / 2) * DEGREES, about_point=ORIGIN)
    arc = Arc(radius=radius, start_angle=(90 + angle / 2 + arc_buff) * DEGREES,
              angle=TAU - (angle * DEGREES + 2 * arc_buff * DEGREES), arc_center=ORIGIN)
    return arc


def coordinate_labels(axes, start, end):
    num_list = VGroup()
    for i in range(start, end + 1):
        if i != 0:
            num_x = DecimalNumber(i, num_decimal_places=0, font_size=20).next_to(axes.x_axis.n2p(i), DOWN)
            num_y = DecimalNumber(i, num_decimal_places=0, font_size=20).next_to(axes.y_axis.n2p(i), LEFT)
            num_list.add(num_x, num_y)
    return num_list


# 该函数中的大部分参数只在调试阶段用到，但以防万一最终还是保留了下来
def zx_axes(angle, str_color=BLUE, player_color=YELLOW, arc_fill=False, arc_radius=0.5, arc_buff=0.2,
            player_buff=0, str_buff=0, axes_height=5, axes_width=5, player_font_size=35, str_font_size=35,
            player_x='x_{1}', player_z='z_{1}', str_x='x_{2}', str_z='z_{2}'):
    axes = Axes(
        x_range=(-5, 5),
        y_range=(-5, 5),
        height=axes_height,
        width=axes_width,
        axis_config={
            "include_tip": True,
            "include_ticks": False,
            "include_numbers": False
        }
    )
    axe_z_text = Tex(r'\mathtt{z}', font_size=45).move_to(axes.c2p(5, 0.5))
    axe_x_text = Tex(r'\mathtt{x}', font_size=45).move_to(axes.c2p(0.5, 5))
    center = Circle(radius=2, color=RED_C)
    center_line = Line(start=np.array([0, 0, 0]), end=np.array([0, 2, 0]), color=GREEN_D
                       ).rotate(angle=-angle * DEGREES, about_point=axes.c2p(0, 0))
    if arc_fill:
        arc_angle = Arc(radius=2, start_angle=90 * DEGREES, angle=-angle * DEGREES, arc_center=ORIGIN,
                        stroke_width=0, color=GREEN_D).set_fill(color=GREEN_D, opacity=0.5).add_line_to(ORIGIN)
    else:
        arc_angle = Arc(radius=arc_radius, start_angle=90 * DEGREES, angle=-angle * DEGREES,
                        arc_center=ORIGIN, color=GREEN_D).add_line_to(ORIGIN)
    rotate_group = VGroup(arc_angle, center_line, center, axes)
    rotate_group.rotate(angle=-90 * DEGREES, about_point=ORIGIN)
    axes.flip(LEFT)
    player = Dot(point=axes.c2p(0, 0), color=player_color)
    stronghold = Dot(point=center_line.get_end(), color=str_color)
    player_pos = Tex(r"\mathtt{({\color[RGB]{255, 255, 0}" + str(player_z) + r"}, {\color[RGB]{255, 255, 0}"
                     + str(player_x) + r"})}", font_size=player_font_size)
    str_pos = Tex(r"\mathtt{({\color[RGB]{88, 196, 221}" + str(str_z) + r"}, {\color[RGB]{88, 196, 221}"
                  + str(str_x) + r"})}", font_size=str_font_size)
    theta = Tex(r"\theta", font_size=36, color=GREEN_D).move_to(
        Arc(radius=arc_radius + arc_buff, angle=-angle * DEGREES,
            arc_center=axes.c2p(0, 0)).point_from_proportion(0.5)
    )
    if -180 <= angle < -90:
        player_pos.next_to(player, RIGHT).shift(DOWN * 0.3 + LEFT * 0.2).shift(player_buff)
        str_pos.next_to(stronghold, LEFT).shift(str_buff)
    elif -90 <= angle < 0:
        player_pos.next_to(player, LEFT).shift(DOWN * 0.3 + RIGHT * 0.2).shift(player_buff)
        str_pos.next_to(stronghold, RIGHT).shift(str_buff)
    elif 0 <= angle < 90:
        player_pos.next_to(player, LEFT).shift(UP * 0.3 + RIGHT * 0.2).shift(player_buff)
        str_pos.next_to(stronghold, RIGHT).shift(str_buff)
    elif 90 <= angle < 180:
        player_pos.next_to(player, RIGHT).shift(UP * 0.3 + LEFT * 0.2).shift(player_buff)
        str_pos.next_to(stronghold, LEFT).shift(str_buff)
    stuff = Group(arc_angle, center_line, center, axes, axe_x_text,
                  axe_z_text, player, stronghold, player_pos, str_pos, theta)
    return stuff


########################################################################################################################
class Scene1(Scene):  # 204
    def waiting(self, second=0, frame=0, fps=60):
        self.wait(second + frame / fps)

    def construct(self):
        bg = ImageMobject('assets\\raster_images\\back3.png', height=8).save_state()
        bg.add_updater(lambda obj: self.bring_to_back(obj))
        axes0 = Axes()
        line_blue = axes0.get_graph(lambda x: 4 * x + 2, color=BLUE_D)
        line_orange = axes0.get_graph(lambda x: -4 * x + 2, color=ORANGE)
        p = line_intersection(
            line_blue.get_start_and_end(),
            line_orange.get_start_and_end()
        )
        cross_point = Dot(point=p, radius=0.07, color=YELLOW_D)
        self.add(line_blue, line_orange)
        self.play(
            AnimationGroup(
                ShowCreation(line_blue, run_time=1.5),
                ShowCreation(line_orange, run_time=1.5),
                lag_ratio=0.25,
                rate_func=rush_from
            )
        )
        self.play(GrowFromCenter(cross_point, run_time=0.25))
        self.waiting(3, 8)

        axes = Axes(
            x_range=(0, 11),
            y_range=(0, 11),
            height=7,
            width=7,
            axis_config={"include_tip": True},
        ).move_to(ORIGIN)
        axes.add_coordinate_labels(
            font_size=20,
            num_decimal_places=0,
        )
        quarter_circle = axes.get_graph(lambda x: np.sqrt(100 - x ** 2), color=BLUE, x_range=[0, 10], stroke_width=1
                                        ).set_color(ORANGE)
        x_ten_dot = axes.c2p(10, 0)
        zero_dot = axes.c2p(0, 0)
        axe_y_text = Tex(r'\mathtt{{y}}').move_to(axes.c2p(0.5, 11))
        axe_x_text = Tex(r'\mathtt{{x}}').move_to(axes.c2p(11, 0.5))
        line_ykx = Line(Dot(point=zero_dot).get_center(), Dot(point=x_ten_dot).get_center()).set_color(BLUE_D)
        line_ykx.rotate(angle=45 * DEGREES, about_point=zero_dot)
        line_ykx_name = Tex(r"\mathtt{{\color[RGB]{41, 171, 202}y}=kx+b\ (k\neq 0)}",
                            font_size=42).move_to(axes.c2p(6, 3))
        line_arc_cross_dot = Dot(point=line_ykx.get_end(), radius=0.07, color=YELLOW_D)
        self.play(
            AnimationGroup(
                ReplacementTransform(line_orange, quarter_circle, run_time=0.5),
                ReplacementTransform(line_blue, line_ykx, run_time=0.5),
                Write(line_ykx_name, run_time=0.75),
                LaggedStart(*[Write(axes), Write(axe_y_text), Write(axe_x_text)], run_time=0.75),
                cross_point.animate.move_to(line_arc_cross_dot),
                lag_ratio=0.005
            ),
            rate_func=rush_from
        )
        self.remove(line_ykx)
        dot_x_ten_dot = Dot(point=x_ten_dot)
        dot_zero_dot = Dot(point=zero_dot)
        line_yx = Line(dot_x_ten_dot.get_center(), dot_zero_dot.get_center()).set_color(BLUE_D)
        line_yx.rotate(angle=45 * DEGREES, about_point=zero_dot)
        self.add(line_yx).bring_to_front(cross_point)
        self.play(
            line_ykx_name[0][2].animate.set_color(RED_D),
            line_ykx_name[0][7].animate.set_color(RED_D)
        )
        axes2 = Axes(
            x_range=(0, 11),
            y_range=(0, 11),
            height=7,
            width=7,
            axis_config={"include_tip": True},
        ).to_edge(ORIGIN)
        axes2.add_coordinate_labels(
            font_size=20,
            num_decimal_places=0,
        )
        axes2.to_edge(LEFT)
        x_ten_dot2 = axes2.c2p(10, 0)
        zero_dot2 = axes2.c2p(0, 0)
        dot_x_ten_dot2 = Dot(point=x_ten_dot2).set_color(RED)
        dot_zero_dot2 = Dot(point=zero_dot2).set_color(BLUE)
        line_yx2 = Line(dot_x_ten_dot2.get_center(), dot_zero_dot2.get_center()).set_color(BLUE_D)
        line_yx2.rotate(angle=45 * DEGREES, about_point=zero_dot2)
        end_dot = Dot(point=line_yx2.get_start(), radius=0.07, color=YELLOW_D)
        f_always(axe_y_text.move_to, lambda: axes.c2p(0.5, 11))
        f_always(axe_x_text.move_to, lambda: axes.c2p(11, 0.5))
        f_always(dot_x_ten_dot.move_to, lambda: axes.c2p(10, 0))
        f_always(quarter_circle.move_to, lambda: axes.c2p(5, 5))
        self.play(
            AnimationGroup(
                axes.animate.to_edge(LEFT),
                ReplacementTransform(line_yx, line_yx2),
                ReplacementTransform(cross_point, end_dot),
                line_ykx_name.animate.to_corner(RIGHT + UP).shift(LEFT * 0.25).scale(1.3),
            ),
            rate_func=rush_from
        )
        self.wait()

        theme = GREEN_C
        degree_label = Arc(radius=0.5, angle=45 * DEGREES, arc_center=axes.c2p(0, 0), color=theme, stroke_width=3
                           ).set_fill(color=theme, opacity=0.5).add_line_to(axes.c2p(0, 0))
        self.bring_to_back(degree_label)
        alpha = Tex(r"\alpha", font_size=36, color=theme).move_to(
            Arc(radius=0.75, angle=45 * DEGREES, arc_center=axes.c2p(0, 0)).point_from_proportion(0.5)
        )
        self.play(
            ShowCreation(degree_label),
            Write(alpha),
            run_time=0.5
        )
        self.wait()

        k_tan = Tex(r'\mathtt{{\color[RGB]{230, 90, 76}k}=\tan {\color[RGB]{119, 176, 93}\alpha}}',
                    font_size=60).arrange(RIGHT).to_edge(RIGHT)
        self.play(
            ReplacementTransform(alpha[0][0].copy(), k_tan[0][5]),
            ReplacementTransform(line_ykx_name[0][2].copy(), k_tan[0][0]),
            Write(k_tan[0][1:5])
        )
        self.wait()

        position = Tex(r"\mathtt{({\color[RGB]{85, 193, 167}5}, {\color[RGB]{85, 193, 167}5})}"
                       ).move_to(axes.c2p(6, 4.5))
        h_line = always_redraw(lambda: axes.get_h_line(end_dot.get_left()))
        v_line = always_redraw(lambda: axes.get_v_line(end_dot.get_bottom()))
        self.play(
            ShowCreation(h_line),
            ShowCreation(v_line),
            rate_func=smooth
        )
        self.play(
            LaggedStart(
                end_dot.animate.move_to(axes.c2p(5, 5)),
                Write(position),
                lag_ratio=0.5,
                rate_func=smooth
            )
        )
        self.wait()

        ta2 = Text('斜截式', font='Source Han Sans HC Light', font_size=50, color=LIGHT_BROWN)
        tb2 = Text('Slope Intercept Form', font='Source Han Sans Light', font_size=25, color=GREY_C, slant=ITALIC)
        tc2 = Tex(r"\mathtt{{\color[RGB]{85, 193, 167}5}=\tan {\color[RGB]{119, 176, "
                  r"93}\alpha}\times {\color[RGB]{85, 193, 167}5}+b}", font_size=30)
        td2 = Tex(r"\mathtt{{\color[RGB]{41, 171, 202}y}={\color[RGB]{230, 90, 76}k}x+b}",
                  font_size=42)
        gb1 = VGroup(tc2, td2).arrange(UP)
        gb2 = VGroup(tb2, ta2).arrange(UP, buff=0.2)
        gb3 = VGroup(gb2, gb1).arrange(RIGHT, buff=0.5)
        box_b = SurroundingRectangle(gb3, buff=0.25, color=YELLOW_E)
        sif = VGroup(gb3, box_b)
        ta1 = Text('点斜式', font='Source Han Sans HC Light', font_size=50, color=LIGHT_BROWN)
        tb1 = Text('Point Slope Form', font='Source Han Sans Light', font_size=25, color=GREY_C, slant=ITALIC)
        tc1 = Tex(r"\mathtt{{\color[RGB]{41, 171, 202}{y}}-{\color[RGB]{85, 193, 167}5}=\tan {"
                  r"\color[RGB]{119, 176, 93}\alpha} \left( x-{\color[RGB]{85, 193, 167}5}\right)}", font_size=30)
        td1 = Tex(r"\mathtt{{\color[RGB]{41, 171, 202}{y}}-{\color[RGB]{85, 193, 167}y_{0}}={\color[RGB]{230, 90, "
                  r"76}k} \left( x-{\color[RGB]{85, 193, 167}x_{0}}\right)}", font_size=42)
        ga1 = VGroup(tc1, td1).arrange(UP)
        ga2 = VGroup(tb1, ta1).arrange(UP, buff=0.2)
        ga3 = VGroup(ga2, ga1).arrange(RIGHT, buff=0.5)
        box_a = SurroundingRectangle(ga3, buff=0.25, color=YELLOW_E)
        psf = VGroup(ga3, box_a)
        VGroup(psf, sif).arrange(UP, buff=1.5).scale(0.9).to_edge(RIGHT).shift(RIGHT * 0.2)
        self.play(
            ReplacementTransform(line_ykx_name[0][0:6], td2[0][0:6]),
            ReplacementTransform(position[0][1].copy(), tc1[0][11]),
            ReplacementTransform(position[0][3].copy(), tc1[0][2]),
            ReplacementTransform(position[0][1].copy(), tc2[0][7]),
            ReplacementTransform(position[0][3].copy(), tc2[0][0]),
            ReplacementTransform(k_tan[0][2:6].copy(), tc1[0][4:8]),
            ReplacementTransform(k_tan[0][2:6], tc2[0][2:6]),
            FadeOut(line_ykx_name[0][6:], RIGHT),
            FadeOut(k_tan[0][:2], LEFT),
            ShowCreation(box_a),
            ShowCreation(box_b),
            Write(tc1[0][0:2]),
            Write(tc1[0][3]),
            Write(tc1[0][8:11]),
            Write(tc1[0][12]),
            Write(tc2[0][1]),
            Write(tc2[0][6]),
            Write(tc2[0][8:10]),
            Write(ta1),
            Write(tb1),
            Write(td1),
            Write(ta2),
            Write(tb2),
            run_time=1
        )
        self.waiting(3, 40)

        self.play(
            tc2[0][9].animate.set_color(YELLOW).scale(1.5),
            td2[0][5].animate.set_color(YELLOW).scale(1.5),
            rate_func=there_and_back
        )
        self.waiting(2, 40)
        self.play(
            FadeOut(sif, UP),
            psf.animate.move_to(ORIGIN).to_edge(RIGHT).shift(RIGHT * 0.2)
        )
        self.waiting(2, 30)


class Scene2(Scene):  # 139
    def construct(self):
        bg = ImageMobject('assets\\raster_images\\back3.png', height=8).save_state()
        bg.add_updater(lambda obj: self.bring_to_back(obj))
        player_left = np.array([-4, -2, 0])
        player_right = np.array([4.25, -2.25, 0])
        eye_left = np.array([-1.05, 2.05, 0])
        eye_right = np.array([0.59, 2.345, 0])
        line_left = Line(eye_left, player_left, color=BLUE_D, buff=25)
        line_right = Line(eye_right, player_right, color=BLUE_D, buff=25)
        player_left_dot = Dot(player_left, color=YELLOW_D, radius=0.07)
        player_right_dot = Dot(player_right, color=YELLOW_D, radius=0.07)
        eye_left_dot = Dot(eye_left, color=YELLOW_D, radius=0.07)
        eye_right_dot = Dot(eye_right, color=YELLOW_D, radius=0.07)
        eye_image_left = ImageMobject(r'assets\raster_images\Eye.webp', height=0.6).next_to(eye_left, LEFT).shift(
            RIGHT * 0.1)
        eye_image_right = ImageMobject(r'assets\raster_images\Eye.webp', height=0.6).next_to(eye_right).shift(
            LEFT * 0.1)
        player_image_left = ImageMobject(r'assets\raster_images\HumanFace.webp', height=0.4).next_to(player_left, LEFT)
        player_image_right = ImageMobject(r'assets\raster_images\HumanFace.webp', height=0.4).next_to(
            player_right).shift(UP * 0.25 + LEFT * 0.1)
        self.bring_to_back(line_left).bring_to_back(line_right)
        self.play(
            ShowCreation(player_left_dot, run_time=0.25),
            ShowCreation(player_right_dot, run_time=0.25),
            ShowCreation(eye_left_dot, run_time=0.25),
            ShowCreation(eye_right_dot, run_time=0.25),
            ShowCreation(line_left, run_time=1.5),
            ShowCreation(line_right, run_time=1.5),
            FadeIn(player_image_left, run_time=1),
            FadeIn(player_image_right, run_time=1),
            FadeIn(eye_image_left, run_time=1),
            FadeIn(eye_image_right, run_time=1),
            rate_func=smooth
        )

        axes = Axes(
            x_range=(-1, 10),
            y_range=(-1, 8),
            height=7.5,
            width=13,
            axis_config={"include_tip": True}
        ).move_to(ORIGIN)
        z_dot = axes.c2p(0.35, 7.75)
        x_dot = axes.c2p(10, 0.5)
        axe_z_text = Tex(r'\mathtt{{z}}').move_to(z_dot)
        axe_x_text = Tex(r'\mathtt{{x}}').move_to(x_dot)
        x0 = axes.get_graph(lambda x: 0, color=BLUE_D)
        cp_left = line_intersection(
            line_left.get_start_and_end(),
            x0.get_start_and_end()
        )
        cp_right = line_intersection(
            line_right.get_start_and_end(),
            x0.get_start_and_end()
        )
        cp_main = line_intersection(
            line_left.get_start_and_end(),
            line_right.get_start_and_end()
        )
        cross_point = Dot(point=cp_main, radius=0.07, color=RED_D)
        left_angle = Arc(radius=0.5, angle=line_left.get_angle(), arc_center=cp_left, color=GREEN_D)
        right_angle = Arc(radius=0.5, angle=line_right.get_angle(), arc_center=cp_right, color=GREEN_D)
        alpha_left = Tex(r"\mathtt{\alpha_{1}}", font_size=36, color=GREEN_D).move_to(
            Arc(radius=0.75, angle=line_left.get_angle(), arc_center=cp_left).point_from_proportion(0.5))
        alpha_right = Tex(r"\mathtt{\alpha_{2}}", font_size=36, color=GREEN_D).move_to(
            Arc(radius=0.75, angle=line_right.get_angle(), arc_center=cp_right).point_from_proportion(0.5))
        position1 = Tex(r"\mathtt{({\color[RGB]{85, 193, 167}x_{1}}, {\color[RGB]{85, 193, 167}z_{1}})}", font_size=36
                        ).next_to(player_left)
        position2 = Tex(r"\mathtt{({\color[RGB]{225, 161, 88}x_{2}}, {\color[RGB]{225, 161, 88}z_{2}})}", font_size=36
                        ).next_to(player_right, LEFT)
        formula = Tex(r"\left\{\begin{matrix} \mathtt{z-{\color[RGB]{85, 193, 167}z_{1}}=\tan {\color[RGB]{119, 176, "
                      r"93}\alpha_{1}} \left( x-{\color[RGB]{85, 193, 167}x_{1}}\right)} \\ \mathtt{z-{\color[RGB]{"
                      r"225, 161, 88}z_{2}}=\tan {\color[RGB]{119, 176, 93}\alpha_{2}} \left( x-{\color[RGB]{225, "
                      r"161, 88}x_{2}}\right)} \end{matrix}\right.", font_size=42).move_to(ORIGIN).shift(DOWN * 1)
        self.bring_to_back(left_angle).bring_to_back(right_angle)
        self.play(
            LaggedStart(*[Write(axes), FadeIn(axe_z_text), FadeIn(axe_x_text)], run_time=0.75),
            ShowCreation(right_angle, run_time=0.5),
            ShowCreation(left_angle, run_time=0.5),
            Write(alpha_right),
            Write(alpha_left),
            Write(position1),
            Write(position2),
            rate_func=smooth
        )
        self.wait()
        self.play(
            ReplacementTransform(position1[0][1:3].copy(), formula[0][14:16]),
            ReplacementTransform(position1[0][4:6].copy(), formula[0][3:5]),
            ReplacementTransform(position2[0][1:3].copy(), formula[0][30:32]),
            ReplacementTransform(position2[0][4:6].copy(), formula[0][19:21]),
            ReplacementTransform(alpha_left[0][0:2].copy(), formula[0][9:11]),
            ReplacementTransform(alpha_right[0][0:2].copy(), formula[0][25:27]),
            Write(formula[0][0:3], run_time=0.5),
            Write(formula[0][5:9], run_time=0.5),
            Write(formula[0][11:14], run_time=0.5),
            Write(formula[0][16], run_time=0.5),
            Write(formula[0][17:19], run_time=0.5),
            Write(formula[0][21:25], run_time=0.5),
            Write(formula[0][27:30], run_time=0.5),
            Write(formula[0][32], run_time=0.5),
            rate_func=smooth
        )
        self.wait()

        axe_group = VGroup(axes, axe_z_text, axe_x_text, formula)
        self.play(
            ReplacementTransform(formula.copy(), cross_point),
            axe_group.animate.set_opacity(0.3),
            self.camera.frame.animate.scale(0.75).move_to(cross_point),
            bg.animate.scale(0.75).move_to(cross_point),
            rate_func=smooth
        )
        self.wait()

        bg.clear_updaters()
        self.play(
            self.camera.frame.animate.scale(0.75).move_to(left_angle).shift(UP * 0.25),
            bg.animate.scale(0.75).move_to(left_angle).shift(UP * 0.25)
        )
        self.wait()
        self.play(position1.animate.set_color(YELLOW_D), rate_func=there_and_back)
        self.wait()
        self.play(
            left_angle.animate.set_color(RED_D),
            alpha_left.animate.set_color(RED_D),
            rate_func=there_and_back
        )
        self.wait()
        self.play(
            self.camera.frame.animate.to_default_state(),
            bg.animate.restore(),
            axe_group.animate.set_opacity(1),
            rate_func=smooth
        )
        self.wait()


class Scene3(Scene):  # 407
    def waiting(self, second=0, frame=0, fps=60):
        self.wait(second + frame / fps)

    def construct(self):
        bg = ImageMobject('assets\\raster_images\\back3.png', height=8).save_state()
        bg.add_updater(lambda obj: self.bring_to_back(obj))
        gird = NumberPlane()
        axes = Axes(
            x_range=(-5, 5),
            y_range=(-5, 5),
            height=7,
            width=7,
            axis_config={
                "include_tip": True,
                "include_ticks": False,
                "include_numbers": False
            }
        ).move_to(ORIGIN)
        axe_z_text = Tex(r'\mathtt{{z}}').move_to(axes.c2p(0.5, 5))
        axe_x_text = Tex(r'\mathtt{{x}}').move_to(axes.c2p(5, 0.5))
        center = Circle(radius=2, color=RED_C).move_to(ORIGIN)
        center_line = Line(gird.c2p(0, 0), gird.c2p(0, 2), color=GREEN_D)
        theme = GREEN_D
        theta_tracker = ValueTracker(0)
        arc_angle = Arc()
        arc_angle.add_line_to(ORIGIN)
        degree = Integer(
            show_ellipsis=False,
            num_decimal_places=0,
            include_sign=False,
            unit=r'^{\circ}',
            font_size=38,
        )
        degree.add_updater(
            lambda x: x.set_value(-theta_tracker.get_value()).set_color(YELLOW_D).move_to(
                Line(start=ORIGIN, end=np.array([0, 2.5, 0])).rotate(
                    angle=theta_tracker.get_value() / 2 * DEGREES, about_point=ORIGIN).get_end()
            )
        )
        center_line.add_updater(
            lambda obj: obj.become(Line(gird.c2p(0, 0), gird.c2p(0, 2)).set_color(theme).rotate(
                angle=(theta_tracker.get_value()) * DEGREES, about_point=ORIGIN))
        )
        arc_angle.add_updater(
            lambda obj: obj.become(
                Arc(radius=2, start_angle=90 * DEGREES, angle=theta_tracker.get_value() * DEGREES, arc_center=ORIGIN,
                    stroke_width=0, color=theme).set_fill(color=theme, opacity=0.5).add_line_to(ORIGIN)
            )
        )
        self.add(axes, axe_x_text, axe_z_text, arc_angle, center_line, center, degree)
        self.play(theta_tracker.animate.set_value(-45), run_time=10, rate_func=linear)
        self.waiting(frame=30)
        self.play(theta_tracker.animate.set_value(45), run_time=10, rate_func=linear)
        self.wait()

        center_line.clear_updaters()
        arc_angle.clear_updaters()
        degree.clear_updaters()
        rotate_group = VGroup(arc_angle, center_line, center, axes)
        arc_trans = Arc(radius=0.5, angle=45 * DEGREES, arc_center=ORIGIN, color=theme, stroke_width=3
                        ).set_fill(color=theme, opacity=0.5).add_line_to(ORIGIN)
        self.play(
            rotate_group.animate.rotate(angle=-90 * DEGREES, about_point=ORIGIN),
            degree.animate.move_to(Line(start=ORIGIN, end=np.array([0, 2.7, 0])).rotate(
                angle=-45 * 1.5 * DEGREES, about_point=ORIGIN).get_end()),
            axe_z_text.animate.move_to(axes.c2p(5, 0.5)),
            axe_x_text.animate.move_to(axes.c2p(0.5, -5)),
            rate_func=smooth
        )
        self.bring_to_back(axes)
        self.play(
            axes.animate.flip(LEFT),
            axe_x_text.animate.move_to(axes.c2p(-5, 0.5)),
            rate_func=smooth
        )
        self.play(
            Indicate(axe_x_text),
            Indicate(axe_z_text)
        )
        self.play(
            Transform(arc_angle, arc_trans),
            degree.animate.move_to(Line(start=ORIGIN, end=np.array([0, 1, 0])).rotate(
                angle=-45 * 1.5 * DEGREES, about_point=ORIGIN).get_end()).shift(DOWN * 0.1).scale(0.75),
            center_line.animate.set_color(BLUE_D),
            center.animate.set_stroke(width=1)
        )
        self.waiting(3, 23)
        bg.clear_updaters()
        self.play(
            self.camera.frame.animate.scale(0.5).move_to(degree),
            bg.animate.scale(0.5).move_to(degree)
        )
        bg.add_updater(lambda obj: self.bring_to_back(obj))
        self.play(degree[0].animate.set_color(RED_E))
        self.wait()

        axes2 = Axes(
            x_range=(-5, 5),
            y_range=(-5, 5),
            height=7,
            width=7,
            axis_config={
                "include_tip": True,
                "include_ticks": False,
                "include_numbers": False
            }
        ).move_to(ORIGIN).to_edge(LEFT)
        arc_angle2 = Arc(radius=0.5, angle=45 * DEGREES, arc_center=axes2.c2p(0, 0), color=theme,
                         stroke_width=3).set_fill(color=theme, opacity=0.5).add_line_to(axes2.c2p(0, 0))
        formula = Tex(r'\mathtt{{\color[RGB]{230, 90, 76}k}=\tan{\color[RGB]{131, 193, 103}\alpha}=\tan\left({\color['
                      r'RGB]{207, 80, 68}-{\color[RGB]{244, 211, 69}\theta}}\right)=\tan\left[{\color[RGB]{207, 80, '
                      r'68}-}\left({\color[RGB]{244, 211, 69}-45^{\circ}}\right)\right]}',
                      font_size=50).to_edge(RIGHT + UP)
        alpha = Tex(r'\mathtt{{\color[RGB]{131, 193, 103}\alpha}}', font_size=38
                    ).move_to(Arc(radius=0.75, angle=45 * DEGREES, arc_center=ORIGIN, color=GREEN_D))
        f_always(center_line.move_to, lambda: axes.c2p(1, 1))
        f_always(axe_z_text.move_to, lambda: axes.c2p(0.5, 5))
        f_always(axe_x_text.move_to, lambda: axes.c2p(5, 0.5))
        f_always(alpha.move_to, lambda: Arc(radius=0.75, angle=45 * DEGREES, arc_center=axes.c2p(0, 0), color=theme))
        f_always(center.move_to, lambda: axes.c2p(0, 0))
        bg.clear_updaters()
        self.play(
            self.camera.frame.animate.to_default_state(),
            bg.animate.restore(),
            ReplacementTransform(degree[0:4], formula[0][21:25]),
            Write(formula[0][0:21]),
            Write(formula[0][25:27]),
            Write(alpha),
            axes.animate.to_edge(LEFT),
            Transform(arc_angle, arc_angle2),
            run_time=1
        )
        self.waiting(5, 50)

        center_1 = formula[0][5].get_center()
        center_2 = formula[0][12].get_center()
        alpha_text = Text('倾斜角', font='Source Han Sans HC Light', font_size=32, color=GREEN_C).shift(
            center_1 + 1.2 * DOWN).add(Arrow(center_1 + 0.3 * DOWN, center_1 + 0.9 * DOWN, buff=0))
        theta_text = Text('玩家视角', font='Source Han Sans HC Light', font_size=32, color=YELLOW_D).shift(
            center_2 + 1.2 * DOWN).add(
            Arrow(center_2 + 0.3 * DOWN, center_2 + 0.9 * DOWN, buff=0))
        self.play(Write(alpha_text), run_time=0.75)
        self.wait()
        self.play(Write(theta_text), run_time=0.75)
        self.wait()

        tan_alpha = Tex(r'\mathtt{\tan{\color[RGB]{131, 193, 103}\alpha}}',
                        font_size=480).set_fill(opacity=0).shift(0.5 * UP)
        tan_alpha[0][0:3].set_stroke(color=WHITE, width=2, opacity=0.2)
        tan_alpha[0][3].set_stroke(color=GREEN_C, width=2, opacity=0.2)
        blackboard = Rectangle(height=9.25, width=18).set_fill(color=GREY_D, opacity=1).move_to(ORIGIN)
        mask = Rectangle(height=9, width=16).set_fill(color=BLACK, opacity=0.5).set_stroke(opacity=0).move_to(ORIGIN)
        tan_axes = Axes(
            x_range=(-PI / 2, PI / 2),
            y_range=(-3, 3),
            height=9.25,
            width=18,
            axis_config={
                "include_tip": True,
                "include_ticks": False,
            }
        ).move_to(ORIGIN)
        param_curve = FunctionGraph(
            lambda x: np.tan(x),
            x_range=(-2 * PI, 2 * PI, PI / 22),
            color=ORANGE,
            stroke_width=3,
            discontinuities=[-1.5 * np.pi, -0.5 * np.pi, 0.5 * np.pi, 1.5 * np.pi],
        )
        tan_alpha_func = formula[0][2:6].copy()
        tan_back = VGroup(blackboard, tan_axes).scale(0.75)
        self.add(formula, mask, tan_back, )
        self.play(
            tan_alpha_func.animate.move_to(tan_alpha).set_fill(
                opacity=0).scale(10).set_stroke(color=GREEN_D, width=2, opacity=0.2),
            FadeIn(tan_back, UP),
            FadeIn(mask),
            run_time=0.5,
            rate_func=smooth
        )
        self.play(ShowCreation(param_curve), run_time=0.5)
        odd_function_cn = Text('奇 函 数', font='Source Han Sans HC Light', font_size=150
                               ).set_fill(opacity=0).set_stroke(color=GREEN_D, width=3.6)
        odd_function_en = Text('Odd Function', font='Source Han Sans HC Light', font_size=45
                               ).set_fill(opacity=0).set_stroke(color=BLUE_D, width=1.3)
        odd_function_text = VGroup(odd_function_en, odd_function_cn).arrange(UP, buff=0.5).move_to(ORIGIN)
        self.play(
            param_curve.animate.scale(0.75),
            tan_alpha_func.animate.scale(0.75),
            tan_axes.animate.scale(0.75),
            blackboard.animate.scale(0.75),
            run_time=0.75,
            rate_func=smooth
        )
        self.add(odd_function_text, param_curve).bring_to_front(param_curve)
        self.play(
            FadeOut(tan_alpha_func, DOWN),
            FadeIn(odd_function_text, DOWN),
            run_time=0.75,
            rate_func=smooth
        )
        self.remove(tan_alpha_func)
        self.wait()
        self.add(mask, blackboard, tan_axes, odd_function_text, param_curve)
        self.play(
            FadeOut(blackboard),
            FadeOut(param_curve),
            FadeOut(tan_axes),
            FadeOut(odd_function_cn),
            FadeOut(odd_function_en),
            FadeOut(mask),
            run_time=0.5
        )
        bg.clear_updaters()
        self.play(
            self.camera.frame.animate.scale(0.5).move_to(formula[0][15]).shift(0.5 * DOWN),
            bg.animate.scale(0.5).move_to(formula[0][15]).shift(0.5 * DOWN),
            formula[0][14:15].animate.set_opacity(0.3),
            formula[0][:7].animate.set_opacity(0.3),
            center.animate.set_stroke(opacity=0.3),
            center_line.animate.set_opacity(0.3),
            alpha_text.animate.set_opacity(0.3),
            theta_text.animate.set_opacity(0.3),
            axe_x_text.animate.set_opacity(0.3),
            axe_z_text.animate.set_opacity(0.3),
            arc_angle.animate.set_opacity(0.3),
            alpha.animate.set_opacity(0.3),
            axes.animate.set_opacity(0.3),
        )
        bg.add_updater(lambda obj: self.bring_to_back(obj))
        formula_3 = Tex(r'\mathtt{', r'{\color[RGB]{230, 90, 76}k}=\tan{\color[RGB]{131, 193, 103}\alpha}=',
                        r'\tan', r'\left(', r'{\color[RGB]{207, 80, 68}-}', r'{\color[RGB]{244, 211, 69}\theta}',
                        r'\right)', r'=', r'\tan', r'\left[', r'{\color[RGB]{207, 80, 68}-}', r'\left(',
                        r'{\color[RGB]{244, 211, 69}-45^{\circ}}', r'\right)', r'\right]', r'}',
                        font_size=50).move_to(formula)
        formula_2 = Tex(r'\mathtt{', r'{\color[RGB]{230, 90, 76}k}=\tan{\color[RGB]{131, 193, 103}\alpha}=',
                        r'{\color[RGB]{207, 80, 68}-}', r'\tan', r'\left(', r'{\color[RGB]{244, 211, 69}\theta}',
                        r'\right)', r'=', r'{\color[RGB]{207, 80, 68}-}', r'\tan', r'\left(',
                        r'{\color[RGB]{244, 211, 69}-45^{\circ}}', r'\right)', r'}', font_size=50).move_to(formula)
        center_3 = formula_2[0][5].get_center()
        center_4 = formula_2[4].get_center()
        alpha_text_tans = Text('倾斜角', font='Source Han Sans HC Light', font_size=32, color=GREEN_C).shift(
            center_3 + 1.2 * DOWN).add(Arrow(center_3 + 0.3 * DOWN, center_3 + 0.9 * DOWN, buff=0))
        theta_text_tans = Text('玩家视角', font='Source Han Sans HC Light', font_size=32, color=YELLOW_D).shift(
            center_4 + 1.2 * DOWN).add(Arrow(center_4 + 0.3 * DOWN, center_4 + 0.9 * DOWN, buff=0))
        alpha_text_tans.set_opacity(0.3)
        theta_text_tans.set_opacity(0.3)
        formula_3[0].set_opacity(0.3)
        formula_3[6].set_opacity(0.3)
        formula_2[0].set_opacity(0.3)
        formula_2[6].set_opacity(0.3)
        self.add(formula_3).remove(formula)
        self.play(
            TransformMatchingTex(formula_3, formula_2, path_arc=90 * DEGREES),
            Transform(alpha_text, alpha_text_tans),
            Transform(theta_text, theta_text_tans)
        )
        bg.clear_updaters()
        self.play(
            self.camera.frame.animate.to_default_state(),
            bg.animate.restore(),
            formula_2.animate.set_opacity(1),
            center.animate.set_stroke(opacity=1),
            center_line.animate.set_opacity(1),
            arc_angle.animate.set_opacity(0.5),
            alpha_text.animate.set_opacity(1),
            theta_text.animate.set_opacity(1),
            axe_x_text.animate.set_opacity(1),
            axe_z_text.animate.set_opacity(1),
            alpha.animate.set_opacity(1),
            axes.animate.set_opacity(1),
            run_time=0.75,
            rate_func=smooth
        )
        bg.add_updater(lambda obj: self.bring_to_back(obj))
        position = Dot(point=center_line.get_end(), radius=0.07, color=YELLOW_D).scale(0.1)
        axes_rotate = Axes(
            x_range=(-5, 5),
            y_range=(-5, 5),
            height=7,
            width=7,
            axis_config={
                "include_tip": True,
                "include_ticks": True,
                "include_numbers": False
            }
        ).to_edge(LEFT)
        h_line = always_redraw(lambda: axes_rotate.get_h_line(position.get_center()))
        v_line = always_redraw(lambda: axes_rotate.get_v_line(position.get_center()))
        num_list = coordinate_labels(axes=axes_rotate, start=-5, end=4)
        num_list[12:14].set_color(color=TEAL_D)
        self.play(
            Write(num_list),
            ShowCreation(h_line),
            ShowCreation(v_line),
            Write(axes_rotate),
            FadeOut(axes),
            position.animate.scale(10),
            run_time=0.75,
            rate_func=smooth
        )
        self.waiting(1, 50)

        ta1 = Text('点斜式', font='Minecraft AE', font_size=50, color=LIGHT_BROWN)
        tb1 = Text('Point Slope Form', font='Source Han Sans Light', font_size=25, color=GREY_C, slant=ITALIC)
        tc1 = Tex(
            r'\mathtt{{x}-{\color[RGB]{85, 193, 167}2}=', r'{\color[RGB]{207, 80, 68}-}', r'\tan',
            r'\left(', r'{\color[RGB]{244, 211, 69}-45^{\circ}}', r'\right)',
            r'\left( z-{\color[RGB]{85, 193, 167}2}\right)}', font_size=30)
        td1 = Tex(r'\mathtt{{x}-{\color[RGB]{85, 193, 167}x_{1}}=', r'{\color[RGB]{207, 80, 68}-}',
                  r'\tan', r'\left(', r'{\color[RGB]{244, 211, 69}\theta}', r'\right)',
                  r' \left( z-{\color[RGB]{85, 193, 167}z_{1}}\right)}', font_size=42)
        ga1 = VGroup(tc1, td1).arrange(UP)
        ga2 = VGroup(tb1, ta1).arrange(UP, buff=0.2)
        ga3 = VGroup(ga2, ga1).arrange(RIGHT, buff=0.5)
        box_a = SurroundingRectangle(ga3, buff=0.25, color=YELLOW_E)
        psf = VGroup(ga3, box_a).scale(0.74).to_edge(RIGHT).shift(RIGHT * 0.3)
        self.play(
            ReplacementTransform(num_list[13].copy(), tc1[0][2]),
            ReplacementTransform(num_list[12].copy(), tc1[6][3]),
            ReplacementTransform(formula_2[7:12].copy(), tc1[1:6]),
            ReplacementTransform(formula_2[1:6].copy(), td1[1:6]),
            FadeIn(td1[0], LEFT),
            FadeIn(td1[6], LEFT),
            FadeIn(tc1[0][0:2], LEFT),
            FadeIn(tc1[0][3], LEFT),
            FadeIn(tc1[6][0:3], LEFT),
            FadeIn(tc1[6][4], LEFT),
            FadeIn(ta1, LEFT),
            FadeIn(tb1, LEFT),
            FadeIn(box_a, LEFT)
        )
        self.waiting(2, 10)
        self.play(
            Indicate(axe_x_text),
            Indicate(axe_z_text),
        )
        self.waiting(1, 40)
        self.play(
            Indicate(td1[0][0]),
            Indicate(td1[0][2:4]),
            Indicate(td1[6][1]),
            Indicate(td1[6][3:5]),
        )
        self.waiting(1, 25)

        final_formula = Tex(r'\left\{\begin{matrix} \mathtt{{x}-{\color[RGB]{85, 193, 167}x_{1}}=-\tan\left({\color['
                            r'RGB]{85, 193, 167}\theta_{1}}\right) \left( z-{\color[RGB]{85, 193, 167}z_{1}}\right)} '
                            r'\\ \mathtt{{x}-{\color[RGB]{225, 161, 88}x_{2}}=-\tan\left({\color[RGB]{225, 161, '
                            r'88}\theta_{2}}\right) \left( z-{\color[RGB]{225, 161, 88}z_{2}}\right)}\end{'
                            r'matrix}\right.', font_size=42)
        title = Text('点 斜 式 交 点 法', font='Minecraft AE', font_size=100,
                     t2c={'点 斜 式': LIGHT_BROWN, '交 点 法': BLUE_C})
        line_title = Line(3 * UP, 3 * UP, color=YELLOW_D)
        VGroup(final_formula, line_title, title).arrange(UP, buff=0.75).move_to(axes_rotate.c2p(0, 0))
        mask.set_fill(opacity=0)
        bg.clear_updaters()
        self.play(
            self.camera.frame.animate.move_to(axes_rotate.c2p(0, 0)),
            bg.animate.move_to(axes_rotate.c2p(0, 0)),
            mask.animate.move_to(axes_rotate.c2p(0, 0)).set_fill(opacity=0.75),
            FadeOut(formula_2, RIGHT),
            FadeOut(alpha_text, RIGHT),
            FadeOut(theta_text, RIGHT),
            FadeOut(psf, RIGHT),
            Write(final_formula[0][0]),
            Write(final_formula[0][12]),
            Write(final_formula[0][20:], run_time=1),
            ReplacementTransform(td1[0][0:5].copy(), final_formula[0][1:6]),
            ReplacementTransform(td1[1][0].copy(), final_formula[0][6]),
            ReplacementTransform(td1[2].copy(), final_formula[0][7:10]),
            ReplacementTransform(td1[3][0].copy(), final_formula[0][10]),
            ReplacementTransform(td1[4][0].copy(), final_formula[0][11]),
            ReplacementTransform(td1[5][0].copy(), final_formula[0][13]),
            ReplacementTransform(td1[6].copy(), final_formula[0][14:20]),
            Transform(ta1.copy(), title[0:3]),
            FadeIn(title[3:], DOWN),
            line_title.animate.put_start_and_end_on(3 * LEFT, 3 * RIGHT).move_to(axes_rotate.c2p(0, 0)),
            rate_func=smooth
        )
        bg.add_updater(lambda obj: self.bring_to_back(obj))
        self.wait()
        self.play(
            AnimationGroup(
                Indicate(final_formula[0][3:5], color=RED),
                Indicate(final_formula[0][11:13], color=RED),
                Indicate(final_formula[0][17:19], color=RED),
                Indicate(final_formula[0][22:24], color=RED),
                Indicate(final_formula[0][30:32], color=RED),
                Indicate(final_formula[0][36:38], color=RED),
                lag_ratio=0.12
            )
        )

        final_formula_eye = final_formula.copy()
        eye_image_a = ImageMobject(r'assets\raster_images\Eye.webp', height=0.6
                                   ).next_to(final_formula_eye[0][19], RIGHT).shift(LEFT * 0.1)
        eye_image_b = ImageMobject(r'assets\raster_images\Eye.webp', height=0.6
                                   ).next_to(final_formula_eye[0][38], RIGHT).shift(LEFT * 0.1)
        Group(final_formula_eye, eye_image_a, eye_image_b).move_to(final_formula)
        self.play(
            Transform(final_formula, final_formula_eye),
            FadeIn(eye_image_a, LEFT),
            FadeIn(eye_image_b, LEFT)
        )
        self.wait()


class Scene4(Scene):  # 74
    def construct(self):
        # gird = NumberPlane()
        # tp = ImageMobject('assets\\raster_images\\teleport.png', height=8)
        # bg = ImageMobject('assets\\raster_images\\position.png', height=8)
        # pp = ImageMobject('assets\\raster_images\\multiwidth.png', height=22).shift(DOWN * 11)
        x_l = Text('255.700', font='Minecraft AE', font_size=14, color=TEAL_D).move_to(np.array([-6.1225, 1.88, 0]))
        z_l = Text('-368.300', font='Minecraft AE', font_size=14, color=TEAL_D).move_to(np.array([-3.6125, 1.88, 0]))
        deg_l = Text('139.0', font='Minecraft AE', font_size=14, color=TEAL_D).move_to(np.array([-2.7, 1.28, 0]))
        x_r = Text('255.700', font='Minecraft AE', font_size=14, color=GOLD_D).move_to(np.array([0.988, 1.88, 0]))
        z_r = Text('-479.700', font='Minecraft AE', font_size=14, color=GOLD_D).move_to(np.array([3.499, 1.88, 0]))
        deg_r = Text('136.6', font='Minecraft AE', font_size=14, color=GOLD_D).move_to(np.array([4.4115, 1.28, 0]))
        data = VGroup(x_l, z_l, deg_l, x_r, z_r, deg_r)
        final_formula = Tex(r'{\color[RGB]{100, 100, 100}\left\{\begin{matrix}\mathtt{{\color[RGB]{100, 100, '
                            r'100} {\color[RGB]{194, 56, 56}{x}}-{\color[RGB]{85, 193, 167}255.7}={\color[RGB]{207, '
                            r'80, 68}-}\tan\left({\color[RGB]{85, 193, 167}139.0^{\circ}}\right) \left[ {\color[RGB]{'
                            r'56, 127, 194}{z}}-\left({\color[RGB]{85, 193, 167}-368.3}\right)\right]}} \\  \mathtt{{'
                            r'\color[RGB]{100, 100, 100} {\color[RGB]{194, 56, 56}{x}}-{\color[RGB]{225, 161, '
                            r'88}255.7}={\color[RGB]{207, 80, 68}-}\tan\left({\color[RGB]{225, 161, 88}136.6^{'
                            r'\circ}}\right) \left[ {\color[RGB]{56, 127, 194}{z}}-\left({\color[RGB]{225, 161, '
                            r'88}-479.7}\right)\right]}} \end{matrix}\right.}',
                            font_size=54).to_edge(DOWN).shift(UP * 1.2)
        func_result = final_formula.copy()
        arrow = Tex(r'{\color[RGB]{100, 100, 100}\Downarrow}', font_size=54)
        cross_location = Tex(r'\mathtt{{\color[RGB]{100, 100, 100}\left({\color[RGB]{194, 56, 56}-943.46},{\color['
                             r'RGB]{56, 127, 194}-1747.78}\right)}}', font_size=54)
        VGroup(cross_location, arrow, func_result).arrange(UP).to_edge(DOWN)
        tp_x = Text('-943.46', font='Minecraft AE', font_size=14, color='#C23838'
                    ).move_to(np.array([-6.168, -3.813, 0]))
        tp_z = Text('-1747.78', font='Minecraft AE', font_size=14, color='#387FC2'
                    ).move_to(np.array([-4.68, -3.813, 0]))
        tp_location = VGroup(tp_x, tp_z)
        self.play(FadeIn(data))
        self.play(
            Write(final_formula[0][0:3]),
            Write(final_formula[0][8:14]),
            Write(final_formula[0][20:25]),
            Write(final_formula[0][31:35]),
            Write(final_formula[0][40:46]),
            Write(final_formula[0][52:57]),
            Write(final_formula[0][63]),
            Write(final_formula[0][64]),
            ReplacementTransform(x_l, final_formula[0][3:8]),
            ReplacementTransform(z_l, final_formula[0][25:31]),
            ReplacementTransform(deg_l, final_formula[0][14:20]),
            ReplacementTransform(x_r, final_formula[0][35:40]),
            ReplacementTransform(z_r, final_formula[0][57:63]),
            ReplacementTransform(deg_r, final_formula[0][46:52]),
        )
        self.wait()
        self.play(
            final_formula.animate.move_to(func_result),
            FadeIn(arrow, DOWN),
            ReplacementTransform(final_formula[0][1:2].copy(), cross_location[0][1:8]),
            ReplacementTransform(final_formula[0][33:34].copy(), cross_location[0][1:8]),
            ReplacementTransform(final_formula[0][22:23].copy(), cross_location[0][9:17]),
            ReplacementTransform(final_formula[0][54:55].copy(), cross_location[0][9:17]),
            FadeIn(cross_location[0][0], DOWN),
            FadeIn(cross_location[0][8], DOWN),
            FadeIn(cross_location[0][17], DOWN),
        )
        self.wait()
        self.play(
            ReplacementTransform(cross_location[0][1:8], tp_x),
            ReplacementTransform(cross_location[0][9:17], tp_z),
            FadeOut(arrow, DOWN),
            FadeOut(final_formula, DOWN),
            FadeOut(cross_location[0][0], DOWN),
            FadeOut(cross_location[0][8], DOWN),
            FadeOut(cross_location[0][17], DOWN),
        )
        self.wait()
        self.play(FadeOut(tp_location))
        self.wait()


class Scene5(Scene):  # 376
    def waiting(self, second=0, frame=0, fps=60):
        self.wait(second + frame / fps)

    def construct(self):
        bg = ImageMobject('assets\\raster_images\\back4.png', height=8)
        bg.add_updater(lambda obj: self.bring_to_back(obj)).save_state()
        c1728 = Circle(radius=3.6608, stroke_width=3, color=RED)
        run_dot = Dot(radius=0.07, color=YELLOW_D).move_to(np.array([3.6608, 0, 0]))
        r1728 = Line(start=np.array([3.6608, 0, 0]), end=ORIGIN, stroke_color=LIGHT_BROWN, stroke_width=5)
        r1728_text = Text('R=1728', font='Source Han Sans HC Light', font_size=28, color=LIGHT_BROWN
                          ).move_to(r1728).shift(UP * 0.3)
        origin_point = Text('世界原点', font='Source Han Sans HC Light',
                            font_size=32, color=YELLOW_D).next_to(ORIGIN, LEFT)
        mask = Rectangle(height=9, width=16).set_fill(color=BLACK, opacity=0.8).set_stroke(opacity=0)
        self.camera.frame.scale(0.6)
        self.add(run_dot)
        trace = TracedPath(run_dot.get_center, stroke_width=3).set_color(RED)
        self.add(trace, run_dot)
        self.play(
            self.camera.frame.animate.to_default_state(),
            MoveAlongPath(run_dot, c1728),
            run_time=0.8,
            rate_func=smooth
        )
        self.remove(trace).add(c1728).bring_to_back(r1728).bring_to_front(run_dot)
        self.play(
            ShowCreation(r1728),
            FadeIn(r1728_text, LEFT),
            AnimationGroup(
                run_dot.animate.move_to(ORIGIN),
                FadeInFromPoint(origin_point, ORIGIN),
                lag_ratio=0.3,
            ),
        )
        self.waiting(frame=15)

        rate = 1.3
        text_1280 = Text('R=1280', font='Source Han Sans HC Light', font_size=18, color=BLUE_B)
        text_1728 = Text('R=1728', font='Source Han Sans HC Light', font_size=18, color=RED)
        text_2816 = Text('R=2816', font='Source Han Sans HC Light', font_size=18, color=BLUE_B)
        arc_text_1280 = arc_text(text=text_1280, radius=1.28 * rate, angle=30, arc_buff=5
                                 ).set_color(color=BLUE_D).set_style(stroke_width=1)
        arc_text_1728 = arc_text(text=text_1728, radius=1.728 * rate, angle=25, arc_buff=4
                                 ).set_color(color=RED).set_style(stroke_width=3)
        arc_text_2816 = arc_text(text=text_2816, radius=2.816 * rate, angle=20, arc_buff=2
                                 ).set_color(color=BLUE_D).set_style(stroke_width=1)
        annulus_fill = Circle(radius=2.048 * rate, stroke_width=153.6 * rate, stroke_opacity=0.5, color=BLUE_D)
        c1728_2 = Arc(radius=3.6608, start_angle=90 * DEGREES, angle=2 * PI, stroke_width=3, color=RED)
        c1728_3 = Arc(radius=3, start_angle=90 * DEGREES, angle=2 * PI, stroke_width=3, color=RED)
        self.bring_to_back(annulus_fill).remove(c1728).add(c1728_2)
        self.play(
            FadeIn(annulus_fill),
            FadeOutToPoint(r1728, run_dot.get_center()),
            ReplacementTransform(r1728_text, text_1728),
            ReplacementTransform(c1728_2, arc_text_1728),
            ShowCreation(arc_text_1280),
            ShowCreation(arc_text_2816),
            Write(text_1280),
            Write(text_2816),
            origin_point.animate.move_to(ORIGIN).shift(DOWN * 0.35),
            run_time=1,
            rate_func=smooth
        )
        self.waiting(frame=40)
        self.play(annulus_fill.animate.set_color(color=YELLOW), rate_func=there_and_back)
        self.waiting(2, 15)
        self.play(ShowCreationThenDestruction(arc_text_1728.copy().set_color(YELLOW)), rate_func=smooth)
        self.waiting(1, 45)
        self.play(Indicate(text_1728))
        self.waiting(2, 5)

        axes = Axes(
            x_range=(-5, 5),
            y_range=(-5, 5),
            height=7,
            width=7,
            axis_config={
                "include_tip": True,
                "include_ticks": False,
                "include_numbers": False
            }
        )
        axe_z_text = Tex(r'\mathtt{{z}}').move_to(axes.c2p(5, 0.5))
        axe_x_text = Tex(r'\mathtt{{x}}').move_to(axes.c2p(0.5, 5))
        cir_formula = Tex(r'\mathtt{z^{2}+x^{2}={\color[RGB]{252, 98, 85}1728}^{2}}',
                          font_size=54).to_corner(RIGHT + UP)
        cir_formula_backup = cir_formula.copy()
        run_dot.add_updater(lambda obj: self.bring_to_front(obj))
        self.play(
            LaggedStart(*[Write(axes), Write(axe_z_text), Write(axe_x_text)], run_time=0.75),
            Write(cir_formula[0][0:6]),
            Write(cir_formula[0][10]),
            Transform(arc_text_1728, c1728_3),
            FadeOutToPoint(text_1280, run_dot.get_center()),
            FadeOutToPoint(text_1728[0:2], run_dot.get_center()),
            ReplacementTransform(text_1728[2:6], cir_formula[0][6:10]),
            FadeOutToPoint(text_2816, run_dot.get_center()),
            FadeOutToPoint(origin_point, run_dot.get_center()),
            FadeOutToPoint(annulus_fill, run_dot.get_center()),
            FadeOutToPoint(arc_text_1280, run_dot.get_center()),
            FadeOutToPoint(arc_text_2816, run_dot.get_center()),
        )
        self.wait()
        self.play(ShowCreationThenDestructionAround(cir_formula))
        self.waiting(4, 30)

        run_dot.clear_updaters()
        r_line = Line(start=ORIGIN, end=np.array([3, 0, 0]))
        pr = ImageMobject(r'assets\raster_images\PortalRoom.webp', height=1.3)
        step = 16
        a = TAU / step
        dot_group = VGroup()
        for tick in range(0, step):
            r_line.rotate(angle=a, about_point=ORIGIN)
            dot_group.add(Dot(point=r_line.get_end(), radius=0.07, color=YELLOW_B))
        count = len(dot_group)
        for i in range(0, count):
            self.play(FadeIn(dot_group[i], ORIGIN), run_time=0.02, rate_func=smooth)
        self.wait()
        pr.move_to(dot_group[13])
        self.play(FadeIn(pr), run_time=0.3, rate_func=smooth)
        self.play(FadeOut(pr), run_time=0.3, rate_func=smooth)
        pr.move_to(dot_group[6])
        self.play(FadeIn(pr), run_time=0.3, rate_func=smooth)
        self.play(FadeOut(pr), run_time=0.3, rate_func=smooth)
        pr.move_to(dot_group[1])
        self.play(FadeIn(pr), run_time=0.3, rate_func=smooth)
        self.wait()

        str_point = Dot(point=r_line.get_end(), radius=0.07, color=TEAL).move_to(dot_group[1])
        line = Line(start=np.array([1, 0, 0]), end=str_point.get_center(), stroke_width=3, color=BLUE_D)
        line_flash = Line(start=np.array([1, 0, 0]), end=str_point.get_center(), stroke_width=3, color=ORANGE)
        line_y0 = Line(start=ORIGIN, end=np.array([1, 0, 0]), stroke_width=3, color=BLUE_D)
        line_circle_cross = Dot(point=np.array([(45 - (48 * np.sqrt(2))) / 41, -(36 + (60 * np.sqrt(2))) / 41, 0]),
                                radius=0.07, color=GOLD)
        line_back = Line(start=np.array([1, 0, 0]), end=line_circle_cross.get_center(), stroke_width=3, color=ORANGE)
        p = line_intersection(
            line.get_start_and_end(),
            line_y0.get_start_and_end()
        )
        angle = Arc(radius=0.3, angle=line.get_angle(), arc_center=p, stroke_width=2, color=GREEN_D
                    ).set_fill(color=GREEN_D, opacity=0.5).add_line_to(p)
        alpha = Tex(r"\alpha", font_size=28, color=GREEN_D).move_to(
            Arc(radius=0.45, angle=line.get_angle(), arc_center=p).point_from_proportion(0.5))
        position = Tex(r"\mathtt{({\color[RGB]{85, 193, 167}z_{1}}, {\color[RGB]{85, 193, 167}x_{1}})}", font_size=28
                       ).next_to(line.get_center(), LEFT)
        all_formula = Tex(r'\left\{\begin{aligned}&\mathtt{z^{2}+x^{2}={\color[RGB]{252, 98, 85}1728}^{2}} '
                          r'\\&\mathtt{x-{\color[RGB]{85, 193, 167}x_{1}}=-\tan\left({\color[RGB]{85, 193, '
                          r'167}\theta}\right) \left(z-{\color[RGB]{85, 193, 167}z_{1}}\right)}\end{aligned}\right.',
                          font_size=28)
        theta_center = all_formula[0][22].get_center()
        theta_text = Text('玩家视角', font='Source Han Sans HC Light', font_size=14, color=YELLOW_D).shift(
            theta_center + 0.75 * DOWN).add(Arrow(theta_center + 0.2 * DOWN, theta_center + 0.6 * DOWN, buff=0))
        player_image = ImageMobject(
            r'assets\raster_images\HumanFace.webp', height=0.3).next_to(line.get_center(), RIGHT).shift(LEFT * 0.05)
        VGroup(theta_text, all_formula).move_to(str_point.get_center())
        mask.move_to(line.get_center())
        self.add(angle, line, c1728_3, dot_group, str_point, pr, run_dot)
        bg.clear_updaters()
        self.play(
            self.camera.frame.animate.scale(0.4).move_to(line.get_center()),
            bg.animate.scale(0.4).move_to(line.get_center()),
            FadeOut(dot_group),
            pr.animate.shift(RIGHT * 0.65 + UP * 0.1).scale(0.5),
            ShowCreation(line),
            ShowCreation(angle),
            Write(alpha),
            FadeInFromPoint(position, line.get_center()),
            LaggedStart(
                run_dot.animate.move_to(line.get_center()),
                GrowFromCenter(player_image, run_time=0.5),
                lag_ratio=0.5,
            ),
            cir_formula.animate.scale(0.43).move_to(str_point).shift(LEFT * 1.2 + UP * 0.1),
            rate_func=smooth
        )
        self.wait()
        self.add(player_image, mask, cir_formula)
        self.play(
            self.camera.frame.animate.move_to(str_point.get_center()),
            bg.animate.move_to(str_point.get_center()),
            FadeIn(mask),
            Write(all_formula[0][0]),
            Write(all_formula[0][12:14]),
            Write(all_formula[0][16:22]),
            Write(all_formula[0][23:27]),
            Write(all_formula[0][29]),
            Write(theta_text),
            player_image.animate.scale(1.2).shift(RIGHT * 0.05),
            pr.animate.scale(1.2).shift(UP * 0.2),
            Transform(cir_formula[0], all_formula[0][1:12]),
            ReplacementTransform(alpha[0][0].copy(), all_formula[0][22]),
            ReplacementTransform(position[0][1:3].copy(), all_formula[0][27:29]),
            ReplacementTransform(position[0][4:6].copy(), all_formula[0][14:16]),
            rate_func=smooth
        )
        self.play(FlashAround(all_formula, stroke_width=2))
        self.waiting(4)
        self.play(
            self.camera.frame.animate.to_default_state(),
            bg.animate.restore(),
            FadeOut(all_formula[0][0], DOWN),
            FadeOut(all_formula[0][12:], DOWN),
            FadeOut(theta_text, DOWN),
            FadeOut(mask),
            Transform(cir_formula, cir_formula_backup),
            position.animate.scale(1.2),
            alpha.animate.scale(1.2),
        )
        self.waiting(1, 10)
        self.play(
            AnimationGroup(
                ShowCreation(line_back),
                GrowFromCenter(line_circle_cross, run_time=0.6),
                lag_ratio=0.5,
            )
        )
        self.waiting(2, 10)

        run_dot.add_updater(lambda obj: self.bring_to_front(obj))
        self.play(
            AnimationGroup(
                AnimationGroup(
                    Uncreate(line_back),
                    FadeOutToPoint(line_circle_cross, line_circle_cross.get_center()),
                ),
                ShowCreation(line_flash),
                AnimationGroup(
                    ShowCreation(line.copy()),
                    Indicate(str_point)
                ),
                lag_ratio=0.5,
            ),
            rate_func=smooth
        )
        self.waiting(1, 20)

        run_dot.clear_updaters()
        mask.move_to(ORIGIN)
        dividing_line = Line(start=np.array([0, -3.5, 0]), end=np.array([0, 3.5, 0]), stroke_width=1, color=GREY_C)
        pos_n135 = zx_axes(angle=-135, arc_radius=0.3, arc_buff=0.3)
        pos_n45 = zx_axes(angle=-45, arc_radius=0.3, arc_buff=0.3)
        pos_p45 = zx_axes(angle=45, arc_radius=0.3, arc_buff=0.3)
        pos_p135 = zx_axes(angle=135, arc_radius=0.3, arc_buff=0.3)
        theta_n180_n90 = Tex(r'{\color[RGB]{119, 176, 93}\mathtt{-180^{\circ}<\theta<-90^{\circ}}}', font_size=50)
        theta_n90_0 = Tex(r'{\color[RGB]{119, 176, 93}\mathtt{-90^{\circ}<\theta<0^{\circ}}}', font_size=50)
        theta_0_p90 = Tex(r'{\color[RGB]{119, 176, 93}\mathtt{0^{\circ}<\theta<90^{\circ}}}', font_size=50)
        theta_p90_p180 = Tex(r'{\color[RGB]{119, 176, 93}\mathtt{90^{\circ}<\theta<180^{\circ}}}', font_size=50)
        xz_n180_n90 = Tex(r'\mathtt{{\color[RGB]{88, 196, 221}x_{2}}>{\color[RGB]{255, 255, 0}x_{1}},{\color[RGB]{88, '
                          r'196, 221}z_{2}}<{\color[RGB]{255, 255, 0}z_{1}}}', font_size=55)
        xz_n90_0 = Tex(r'\mathtt{{\color[RGB]{88, 196, 221}x_{2}}>{\color[RGB]{255, 255, 0}x_{1}},{\color[RGB]{88, '
                       r'196, 221}z_{2}}>{\color[RGB]{255, 255, 0}z_{1}}}', font_size=55)
        xz_0_p90 = Tex(r'\mathtt{{\color[RGB]{88, 196, 221}x_{2}}<{\color[RGB]{255, 255, 0}x_{1}},{\color[RGB]{88, '
                       r'196, 221}z_{2}}>{\color[RGB]{255, 255, 0}z_{1}}}', font_size=55)
        xz_p90_p180 = Tex(r'\mathtt{{\color[RGB]{88, 196, 221}x_{2}}<{\color[RGB]{255, 255, 0}x_{1}},{\color[RGB]{88, '
                          r'196, 221}z_{2}}<{\color[RGB]{255, 255, 0}z_{1}}}', font_size=55)
        player_symbol = Dot(radius=0.1, color=YELLOW)
        target_symbol = Dot(radius=0.1, color=BLUE)
        theta = Tex(r"\theta", font_size=36, color=GREEN_D)
        player_text = Text('玩家位置', font='Source Han Sans HC Light', font_size=25)
        target_text = Text('目标要塞', font='Source Han Sans HC Light', font_size=25)
        theta_text = Text('游戏视角', font='Source Han Sans HC Light', font_size=25)
        player_group = VGroup(player_symbol, player_text).arrange(RIGHT)
        target_group = VGroup(target_symbol, target_text).arrange(RIGHT)
        theta_group = VGroup(theta, theta_text).arrange(RIGHT)
        keys_str = VGroup(target_group, player_group, theta_group).arrange(DOWN).to_corner(LEFT + UP * 0.5)
        theta_xz_n180_n90 = Group(theta_n180_n90, xz_n180_n90).arrange(DOWN)
        theta_xz_n90_0 = Group(theta_n90_0, xz_n90_0).arrange(DOWN)
        theta_xz_0_p90 = Group(theta_0_p90, xz_0_p90).arrange(DOWN)
        theta_xz_p90_p180 = Group(theta_p90_p180, xz_p90_p180).arrange(DOWN)
        pos_n135_text = Group(pos_n135, theta_xz_n180_n90).arrange(DOWN)
        pos_n45_text = Group(pos_n45, theta_xz_n90_0).arrange(DOWN)
        pos_p45_text = Group(pos_p45, theta_xz_0_p90).arrange(DOWN)
        pos_p135_text = Group(pos_p135, theta_xz_p90_p180).arrange(DOWN)
        dividing_line1 = dividing_line.copy().reverse_points()
        dividing_line2 = dividing_line.copy().reverse_points()
        dividing_line3 = dividing_line.copy().reverse_points()
        dividing_line_group = Group(dividing_line1, dividing_line2, dividing_line3)
        pos_choose = Group(pos_n135_text, dividing_line1, pos_n45_text, dividing_line2, pos_p45_text, dividing_line3,
                           pos_p135_text).arrange(RIGHT, buff=0.2).scale(0.6)
        self.play(
            FadeIn(mask),
            AnimationGroup(
                AnimationGroup(
                    FadeIn(pos_n135, DOWN),
                    FadeIn(theta_xz_n180_n90, UP),
                ),
                AnimationGroup(
                    FadeIn(pos_n45, DOWN),
                    FadeIn(theta_xz_n90_0, UP),
                ),
                AnimationGroup(
                    FadeIn(pos_p45, DOWN),
                    FadeIn(theta_xz_0_p90, UP),
                ),
                AnimationGroup(
                    FadeIn(pos_p135, DOWN),
                    FadeIn(theta_xz_p90_p180, UP),
                ),
                lag_ratio=0.1,
            ),
            FadeIn(keys_str, RIGHT),
            ShowCreation(dividing_line_group),
            rate_func=smooth
        )
        self.waiting(1, 40)
        self.play(
            Indicate(pos_n135[6], color=RED),
            Indicate(pos_n45[6], color=RED),
            Indicate(pos_p45[6], color=RED),
            Indicate(pos_p135[6], color=RED),
        )
        self.play(
            Indicate(pos_n135[4]),
            Indicate(pos_n135[5]),
            Indicate(pos_n45[4]),
            Indicate(pos_n45[5]),
            Indicate(pos_p45[4]),
            Indicate(pos_p45[5]),
            Indicate(pos_p135[4]),
            Indicate(pos_p135[5]),
        )
        self.waiting(1)
        self.play(
            AnimationGroup(
                ShowCreationThenDestructionAround(theta_xz_n180_n90),
                ShowCreationThenDestructionAround(theta_xz_n90_0),
                ShowCreationThenDestructionAround(theta_xz_0_p90),
                ShowCreationThenDestructionAround(theta_xz_p90_p180),
                lag_ratio=0.2
            )
        )
        self.waiting(2, 20)
        self.play(
            FadeOut(pos_choose, DOWN),
            FadeOut(keys_str, LEFT),
            FadeOut(mask),
            rate_func=smooth
        )

        final_formula = Tex(r'\left\{\begin{aligned}&\mathtt{z^{2}+x^{2}={\color[RGB]{252, 98, 85}1728}^{2}} '
                            r'\\&\mathtt{x-{\color[RGB]{85, 193, 167}x_{1}}=-\tan\left({\color[RGB]{85, 193, '
                            r'167}\theta}\right) \left(z-{\color[RGB]{85, 193, 167}z_{1}}\right)}\end{'
                            r'aligned}\right.', font_size=42)
        title = Text('点 斜 式 估 算 法', font='Minecraft AE', font_size=100,
                     t2c={'点 斜 式': LIGHT_BROWN, '估 算 法': GREEN_D})
        line_title = Line(3 * UP, 3 * UP, color=YELLOW_D)
        VGroup(final_formula, line_title, title).arrange(UP, buff=0.75).move_to(axes.c2p(0, 0))
        mask.set_fill(opacity=0.75).move_to(axes.c2p(0, 0))
        final_formula_eye = final_formula.copy()
        eye_image = ImageMobject(r'assets\raster_images\Eye.webp', height=0.6
                                 ).next_to(final_formula_eye[0][0], LEFT).shift(RIGHT * 0.1)
        Group(final_formula_eye, eye_image).move_to(final_formula)
        self.play(
            FadeIn(mask),
            line_title.animate.put_start_and_end_on(3 * LEFT, 3 * RIGHT).move_to(axes.c2p(0, 0)),
            ReplacementTransform(cir_formula[0], final_formula[0][1:12]),
            Write(final_formula[0][0], run_time=1),
            Write(final_formula[0][12:], run_time=1),
            FadeIn(title, DOWN),
            rate_func=smooth,
        )
        self.wait()
        self.play(
            final_formula.animate.move_to(final_formula_eye),
            FadeInFromPoint(eye_image, final_formula_eye[0][0].get_center())
        )
        self.waiting(frame=30)
        self.play(
            AnimationGroup(
                Indicate(final_formula[0][14:16]),
                Indicate(final_formula[0][22]),
                Indicate(final_formula[0][27:29]),
                lag_ratio=0.25
            )
        )
        self.wait()


class Scene6(Scene):  # 138
    def waiting(self, second=0, frame=0, fps=60):
        self.wait(second + frame / fps)

    def construct(self):
        # gird = NumberPlane()
        # tp = ImageMobject('assets\\raster_images\\teleport2.png', height=8)
        # bg = ImageMobject('assets\\raster_images\\position2.png', height=8)
        # pp = ImageMobject('assets\\raster_images\\multiwidth.png', height=22).shift(LEFT * 6)
        x = Text('-175.700', font='Minecraft AE', font_size=14, color=TEAL_D).move_to(np.array([-6.055, 1.88, 0]))
        z = Text('160.300', font='Minecraft AE', font_size=14, color=TEAL_D).move_to(np.array([-3.545, 1.88, 0]))
        deg = Text('114.0', font='Minecraft AE', font_size=14, color=TEAL_D).move_to(np.array([-2.83, 1.28, 0]))
        final_formula = Tex(r'{\color[RGB]{100, 100, 100} \left\{\begin{aligned}& \mathtt{{\color[RGB]{194, 56, '
                            r'56}{x}}^{2}+{\color[RGB]{56, 127, 194}{z}}^{2} = 1728^{2}}\\& \mathtt{{\color[RGB]{194, '
                            r'56, 56}{x}}+{\color[RGB]{85, 193, 167}175.7} = -\tan\left({\color[RGB]{85, 193, '
                            r'167}114.0^{\circ}}\right) \left({\color[RGB]{56, 127, 194}{z}}-{\color[RGB]{85, 193, '
                            r'167}160.3}\right)}\end{aligned}\right.}', font_size=42).to_edge(LEFT)
        formula_result = final_formula.copy()
        formula_result2 = final_formula.copy()
        arrow = Tex(r'{\color[RGB]{100, 100, 100}\Downarrow}', font_size=42)
        cross_location = Tex(r'\mathtt{{\color[RGB]{100, 100, 100}({\color[RGB]{194, 56, 56}-1654.63},{\color[RGB]{'
                             r'56, 127, 194}-498.16})\ ,\ ({\color[RGB]{194, 56, 56}1477.37},{\color[RGB]{56, 127, '
                             r'194}896.3})}}', font_size=42)
        cross_location_result = cross_location.copy()
        tp_x = Text('-1654.63', font='Minecraft AE', font_size=14, color='#C23838'
                    ).move_to(np.array([-6.10, -3.813, 0]))
        tp_z = Text('-498.16', font='Minecraft AE', font_size=14, color='#387FC2'
                    ).move_to(np.array([-4.61, -3.813, 0]))
        VGroup(cross_location, arrow, formula_result).arrange(UP).to_edge(LEFT)
        VGroup(tp_x, tp_z)
        data = VGroup(x, z, deg)
        self.play(FadeIn(data))
        self.wait()
        self.play(
            Write(final_formula[0][0:14]),
            Write(final_formula[0][19:25]),
            Write(final_formula[0][31:35]),
            Write(final_formula[0][40]),
            ReplacementTransform(x, final_formula[0][14:19]),
            ReplacementTransform(z, final_formula[0][35:40]),
            ReplacementTransform(deg, final_formula[0][25:31]),
        )
        self.waiting(2, 35)
        self.play(
            final_formula.animate.move_to(formula_result),
            FadeInFromPoint(arrow, formula_result.get_bottom()),
            ReplacementTransform(final_formula[0][1:2].copy(), cross_location[0][1:9]),
            ReplacementTransform(final_formula[0][1:2].copy(), cross_location[0][20:27]),
            ReplacementTransform(final_formula[0][12:13].copy(), cross_location[0][1:9]),
            ReplacementTransform(final_formula[0][12:13].copy(), cross_location[0][20:27]),
            ReplacementTransform(final_formula[0][4:5].copy(), cross_location[0][10:17]),
            ReplacementTransform(final_formula[0][4:5].copy(), cross_location[0][28:33]),
            ReplacementTransform(final_formula[0][33:34].copy(), cross_location[0][10:17]),
            ReplacementTransform(final_formula[0][33:34].copy(), cross_location[0][28:33]),
            FadeIn(cross_location[0][0], DOWN),
            FadeIn(cross_location[0][9], DOWN),
            FadeIn(cross_location[0][17:20], DOWN),
            FadeIn(cross_location[0][27], DOWN),
            FadeIn(cross_location[0][33], DOWN),
        )
        self.waiting(1, 20)

        axes = Axes(
            x_range=(-5, 5),
            y_range=(-5, 5),
            height=5,
            width=5,
            axis_config={
                "include_tip": True,
                "include_ticks": False,
                "include_numbers": False,
                "color": "#646464"
            }
        )
        axe_z_text = Tex(r'\mathtt{{\color[RGB]{100, 100, 100}z}}', font_size=45).move_to(axes.c2p(5, 0.5))
        axe_x_text = Tex(r'\mathtt{{\color[RGB]{100, 100, 100}x}}', font_size=45).move_to(axes.c2p(0.5, 5))
        center = Circle(radius=2, color=RED_C)
        center_line = Line(start=np.array([0, 0, 0]), end=np.array([0, 2, 0]), color=GREEN_D
                           ).rotate(angle=-114 * DEGREES, about_point=axes.c2p(0, 0))
        arc_angle = Arc(radius=0.3, start_angle=90 * DEGREES, angle=-114 * DEGREES, arc_center=ORIGIN,
                        color=GREEN_D).add_line_to(ORIGIN)
        rotate_group = VGroup(arc_angle, center_line, center, axes)
        rotate_group.rotate(angle=-90 * DEGREES, about_point=ORIGIN)
        axes.flip(LEFT)
        player = Dot(point=axes.c2p(0, 0), color=YELLOW)
        stronghold = Dot(point=center_line.get_end(), color=BLUE)
        player_pos = Tex(r"\mathtt{{\color[RGB]{100, 100, 100}({\color[RGB]{255, 255, 0}160.3},"
                         r"{\color[RGB]{255, 255, 0}-175.7})}}", font_size=25)
        str_pos = Tex(r"\mathtt{{\color[RGB]{100, 100, 100}({\color[RGB]{56, 127, 194}-498.16},"
                      r"{\color[RGB]{194, 56, 56}-1654.63})}}", font_size=35)
        theta = Tex(r"{\color[RGB]{85, 193, 167}114.0^{\circ}}", font_size=36).move_to(
            Arc(radius=1.1, angle=-114 * DEGREES, arc_center=axes.c2p(0, 0))).shift(RIGHT * 0.2)
        player_pos.next_to(player, RIGHT).shift(UP * 0.2 + LEFT * 0.2)
        str_pos.next_to(stronghold, LEFT).shift(DOWN * 0.2)
        stuff = Group(axes, arc_angle, center_line, center, axe_x_text, axe_z_text,
                      player, stronghold, player_pos, str_pos, theta)
        Group(stuff, cross_location_result, formula_result2).arrange(UP).to_edge(LEFT)
        player_symbol = Dot(radius=0.1, color=YELLOW)
        target_symbol = Dot(radius=0.1, color=BLUE)
        player_text = Text('玩家位置：', font='Source Han Sans HC Light', font_size=25, color='#646464')
        target_text = Text('目标要塞：', font='Source Han Sans HC Light', font_size=25, color='#646464')
        player_group = VGroup(player_symbol, player_text).arrange(LEFT)
        target_group = VGroup(target_symbol, target_text).arrange(LEFT)
        keys = VGroup(target_group, player_group).arrange(UP).move_to(np.array([-5.5, 0.8, 0]))
        self.play(
            final_formula.animate.move_to(formula_result2),
            cross_location[0][:18].animate.move_to(cross_location_result[0][:18]),
            cross_location[0][18:34].animate.move_to(cross_location_result[0][18:34]).set_opacity(0.5),
            FadeOut(arrow, UP),
            FadeIn(stuff[0:9], UP),
            FadeIn(stuff[10], UP),
            FadeIn(stuff[9][0][0], UP),
            FadeIn(stuff[9][0][8], UP),
            FadeIn(stuff[9][0][17], UP),
            ReplacementTransform(cross_location[0][1:9].copy(), stuff[9][0][9:17]),
            ReplacementTransform(cross_location[0][10:17].copy(), stuff[9][0][1:8]),
            FadeIn(keys, RIGHT),
            rate_func=smooth
        )
        self.wait()
        self.play(
            ReplacementTransform(cross_location[0][1:9], tp_x),
            ReplacementTransform(cross_location[0][10:17], tp_z),
            FadeOut(cross_location[0][0], LEFT),
            FadeOut(cross_location[0][9], LEFT),
            FadeOut(cross_location[0][17:], LEFT),
            FadeOut(final_formula, LEFT),
            FadeOut(keys, LEFT),
            FadeOut(stuff, LEFT),
            rate_func=smooth
        )
        self.waiting(frame=30)
        self.play(
            FadeOut(tp_x),
            FadeOut(tp_z),
            run_time=0.5
        )
        self.wait()


class Scene7(Scene):  # 136
    def waiting(self, second=0, frame=0, fps=60):
        self.wait(second + frame / fps)

    def construct(self):
        rate = 1.3
        overworld = ImageMobject('assets\\raster_images\\overworld.png', height=8, opacity=0.75)
        bg = ImageMobject('assets\\raster_images\\back3.png', height=8).save_state()
        bg.add_updater(lambda obj: self.bring_to_back(obj))
        run_dot = Dot(radius=0.07, color=YELLOW_D).move_to(ORIGIN)
        origin_point = Text('世界原点', font='Source Han Sans HC Light',
                            font_size=32, color=YELLOW_D).move_to(ORIGIN).shift(DOWN * 0.35)
        text_1280 = Text('R=1280', font='Source Han Sans HC Light', font_size=18, color=BLUE_B)
        text_1728 = Text('R=1728', font='Source Han Sans HC Light', font_size=18, color=RED)
        text_2816 = Text('R=2816', font='Source Han Sans HC Light', font_size=18, color=BLUE_B)
        arc_text_1280 = arc_text(text=text_1280, radius=1.28 * rate, angle=30, arc_buff=5
                                 ).set_color(color=BLUE_D).set_style(stroke_width=1)
        arc_text_1728 = arc_text(text=text_1728, radius=1.728 * rate, angle=25, arc_buff=4
                                 ).set_color(color=RED).set_style(stroke_width=3)
        arc_text_2816 = arc_text(text=text_2816, radius=2.816 * rate, angle=20, arc_buff=2
                                 ).set_color(color=BLUE_D).set_style(stroke_width=1)
        annulus_fill = Circle(radius=2.048 * rate, stroke_width=153.6 * rate, stroke_opacity=0.5, color=BLUE_D)
        dot_1728 = Dot(radius=0.07, color=RED).move_to(np.array([-1.728 * rate, 0, 0]))
        dot_2816 = Dot(radius=0.07, color=BLUE_D).move_to(np.array([-2.816 * rate, 0, 0]))
        distance = Line(start=dot_1728.get_center(), end=dot_2816.get_center())
        distance_line = Line(start=ORIGIN, end=ORIGIN).move_to(distance.get_center())
        self.add(overworld, run_dot, annulus_fill, text_1728, arc_text_1728,
                 arc_text_1280, arc_text_2816, text_1280, text_2816, origin_point)
        bg.clear_updaters()
        self.play(
            self.camera.frame.animate.scale(0.4).move_to(distance.get_center()).shift(UP * 0.45),
            bg.animate.scale(0.4).move_to(distance.get_center()).shift(UP * 0.45),
            distance_line.animate.put_start_and_end_on(distance.get_end(), distance.get_start()),
            Rotating(arc_text_1728, angle=66 * DEGREES, run_time=1, rate_func=smooth),
            Rotating(text_1728, angle=66 * DEGREES, run_time=1, rate_func=smooth),
            Rotating(arc_text_2816, angle=72 * DEGREES, run_time=1, rate_func=smooth),
            Rotating(text_2816, angle=72 * DEGREES, run_time=1, rate_func=smooth),
            GrowFromCenter(dot_1728),
            GrowFromCenter(dot_2816)
        )
        self.wait()

        axes = Axes(
            x_range=(-5, 5),
            y_range=(-5, 5),
            height=7,
            width=7,
            axis_config={
                "include_tip": True,
                "include_ticks": False,
                "include_numbers": False
            }
        )
        axe_z_text = Tex(r'\mathtt{{z}}').move_to(axes.c2p(5, 0.5))
        axe_x_text = Tex(r'\mathtt{{x}}').move_to(axes.c2p(0.5, 5))
        r1728 = Circle(radius=3, stroke_width=3, color=RED).rotate(angle=156 * DEGREES)
        player1 = Dot(point=np.array([1, -2, 0]), radius=0.07, color=YELLOW)
        player2 = Dot(point=np.array([(3 * np.sqrt(2)) / 2, (3 * np.sqrt(2)) / 2, 0]), radius=0.05, color=BLUE)
        str_temp = Dot(point=np.array([(np.sqrt(65) / 10) + (3 / 2), (3 * np.sqrt(65) / 10) - (1 / 2), 0]),
                       radius=0.07, color=GOLD)
        str_fina = Dot(point=np.array([2.5, 2.5, 0]), radius=0.05, color=GREEN)
        line_p1st = Line(start=player1.get_center(), end=str_temp.get_center(), color=WHITE)
        line_stsf = Line(start=str_temp.get_center(), end=str_fina.get_center(), color=WHITE, stroke_width=3)
        line_p2sf = Line(start=player2.get_center(), end=str_fina.get_center(), color=WHITE, stroke_width=3)
        player1_text = Text('一次测量点', font='Source Han Sans HC Light', font_size=24,
                            color=YELLOW).next_to(player1, LEFT, buff=0.1)
        axes_group = VGroup(axe_z_text, axe_x_text, axes)
        fadeout = [overworld, annulus_fill, text_1728, dot_1728, distance_line, run_dot, text_1280, arc_text_1280,
                   arc_text_2816, arc_text_1728, text_2816, origin_point, dot_2816]
        self.play(
            self.camera.frame.animate.to_default_state(),
            bg.animate.restore(),
            * [FadeOut(mob) for mob in fadeout],
            AnimationGroup(
                GrowFromCenter(axes_group),
                ReplacementTransform(arc_text_1728, r1728),
                AnimationGroup(
                    FadeInFromPoint(player1_text, player1.get_center()),
                    ShowCreation(line_p1st),
                    GrowFromCenter(player1, run_time=0.5),
                ),
                GrowFromCenter(str_temp, run_time=0.5),
                lag_ratio=0.5,
            ),
            rate_func=smooth
        )
        bg.add_updater(lambda obj: self.bring_to_back(obj))
        self.bring_to_back(r1728).bring_to_back(axes)
        self.waiting(frame=30)

        pr = ImageMobject(r'assets\raster_images\PortalRoom.webp',
                          height=0.7).next_to(str_fina, UP, buff=0.05)
        player2_text = Text('二次测量点', font='Source Han Sans HC Light',
                            font_size=16, color=BLUE).next_to(player2, LEFT, buff=0.1)
        str_temp_text = Text('估算要塞', font='Source Han Sans HC Light',
                             font_size=16, color=GOLD).next_to(str_temp, RIGHT, buff=0.1)
        str_fina_text = Text('误差补正要塞', font='Source Han Sans HC Light',
                             font_size=16, color=GREEN).next_to(str_fina, RIGHT, buff=0.1)
        size = ValueTracker(0.07)
        str_temp.add_updater(lambda obj: obj.become(
            Dot(point=np.array([(np.sqrt(65) / 10) + (3 / 2), (3 * np.sqrt(65) / 10) - (1 / 2), 0]),
                radius=size.get_value(), color=GOLD)))
        str_temp.add_updater(lambda obj: self.bring_to_front(obj))
        bg.clear_updaters()
        self.play(
            self.camera.frame.animate.scale(0.4).move_to(str_temp.get_center()).shift(UP * 0.35),
            bg.animate.scale(0.4).move_to(str_temp.get_center()).shift(UP * 0.35),
            r1728.animate.set_style(stroke_width=0.5),
            line_p1st.animate.set_style(stroke_width=3),
            GrowFromCenter(player2),
            size.animate.set_value(0.05),
            FadeInFromPoint(player2_text, player2.get_center()),
            FadeInFromPoint(str_temp_text, str_temp.get_center()),
            rate_func=smooth
        )
        bg.add_updater(lambda obj: self.bring_to_back(obj))
        self.waiting(frame=25)

        player2.add_updater(lambda obj: self.bring_to_front(obj))
        self.play(
            AnimationGroup(
                AnimationGroup(
                    ShowCreation(line_stsf),
                    ShowCreation(line_p2sf),
                ),
                GrowFromCenter(str_fina),
                lag_ratio=0.5,
            ),
            rate_func=smooth
        )
        self.play(
            Indicate(str_fina),
            FadeInFromPoint(pr, str_fina.get_center()),
            FadeInFromPoint(str_fina_text, str_fina.get_center())
        )
        self.waiting(4, 10)


class Scene8(Scene):  # 60
    def construct(self):
        bg = ImageMobject('assets\\raster_images\\back3.png', height=8).save_state()
        bg.add_updater(lambda obj: self.bring_to_back(obj))
        no_tan = Text('斜率不存在', font='Source Han Sans HC Light', font_size=120)
        tittle = Text('斜率不存在', font='Source Han Sans HC Light', font_size=46)
        VGroup(*[no_tan[item] for item in range(0, 5)]).arrange(RIGHT, buff=7)
        VGroup(*[tittle[item] for item in range(0, 5)]).arrange(RIGHT, buff=0.5).next_to(3.05 * UP, UP)
        self.play(FadeIn(no_tan), run_time=0.5)
        weight = ValueTracker(7)
        no_tan.add_updater(lambda obj: obj.arrange(RIGHT, buff=weight.get_value()))
        self.play(weight.animate.set_value(1), run_time=1, rate_func=smooth)
        self.wait()

        no_tan.clear_updaters()
        line_title = Line(3.1 * UP, 3.1 * UP, color=YELLOW)
        axes = Axes(
            x_range=(0, 11),
            y_range=(0, 11),
            height=5,
            width=5,
            axis_config={
                "include_tip": True,
                "include_ticks": True,
                "include_numbers": False
            }
        )
        coord_list = coordinate_labels(axes=axes, start=0, end=10)
        axe_x_text = Tex(r'\mathtt{{x}}').move_to(axes.c2p(0.75, 11))
        axe_z_text = Tex(r'\mathtt{{z}}').move_to(axes.c2p(11, 0.75))
        line = Line(start=axes.c2p(5, 0), end=axes.c2p(5, 10), color=GREEN)
        elbow_line_z = Line(start=axes.c2p(5.5, 0), end=axes.c2p(5.5, 0.5), color=ORANGE)
        elbow_line_x = Line(start=axes.c2p(5, 0.5), end=axes.c2p(5.5, 0.5), color=ORANGE)
        elbow = VGroup(elbow_line_x, elbow_line_z)
        self.play(
            AnimationGroup(
                ReplacementTransform(no_tan, tittle),
                line_title.animate.put_start_and_end_on(3.1 * UP + 6 * LEFT, 3.1 * UP + 6 * RIGHT),
                LaggedStart(*[Write(axes), Write(axe_x_text), Write(axe_z_text), Write(coord_list)], run_time=0.75),
                AnimationGroup(
                    ShowCreation(elbow),
                    ShowCreation(line),
                ),
                ShowCreationThenDestruction(line.copy().set_color(color=YELLOW)),
                lag_ratio=0.5,
            ),
            rate_func=smooth
        )
        self.wait()

        func = Tex(r'\mathtt{{\color[RGB]{131, 193, 103}z}={\color[RGB]{85, 193, 167}5}}',
                   font_size=48).next_to(line, RIGHT)
        self.play(
            coord_list[8].animate.set_color(color=TEAL_D),
            Transform(coord_list[8].copy(), func[0][2]),
            Transform(axe_z_text[0].copy(), func[0][0]),
            Write(func[0][1]),
            rate_func=smooth
        )
        self.wait()


class Scene9(Scene):  # 137
    def construct(self):
        def arc_updater(rate):
            return lambda obj: obj.become(Arc(
                radius=-0.16 + (0.48 * rate), start_angle=90 * DEGREES, angle=path.get_value() * DEGREES,
                stroke_width=24, color='#8eba89', arc_center=ORIGIN).set_style(stroke_opacity=0.5))

        def stroke_updater(rate_a, rate_b):
            return lambda obj: obj.become(Arc(
                radius=rate_b + (0.48 * rate_a), start_angle=90 * DEGREES, angle=path.get_value() * DEGREES,
                stroke_width=1, color=BLUE_D, arc_center=ORIGIN))

        bg = ImageMobject('assets\\raster_images\\back4.png', height=8)
        bg.add_updater(lambda obj: self.bring_to_back(obj))
        path = ValueTracker(360)
        circle_group = VGroup(*[Arc().add_updater(arc_updater(rate)) for rate in range(1, 9)])
        stroke_group = VGroup(*[Arc().add_updater(stroke_updater(rate_a, rate_b))
                                for rate_a in range(1, 9) for rate_b in [-0.04, -0.28]])
        circle_group_uneffect = circle_group.copy().clear_updaters()
        stroke_group_uneffect = stroke_group.copy().clear_updaters()
        origin_point = Dot(radius=0.07, color=YELLOW_D).move_to(ORIGIN)
        circle_symbol = Circle(radius=0.1, stroke_width=5, color='#8EBA89').move_to(np.array([-5.1, 3.5, 0]))
        origin_symbol = Dot(radius=0.1, color=YELLOW_D).move_to(np.array([-5.1, 3.0, 0]))
        symbol_text = Text('要塞分布 ', font='Source Han Sans HC Light', font_size=25).move_to(
            np.array([-6, 3.5, 0])).to_edge(LEFT)
        origin_text = Text('世界原点 ', font='Source Han Sans HC Light', font_size=25).move_to(
            np.array([-6, 3.0, 0])).to_edge(LEFT)
        radius_text = Text('内径 ~ 外径 (单位：格)', font='Source Han Sans HC Light', font_size=25,
                           t2c={'内径 ~ 外径': TEAL, '(单位：格)': WHITE}).move_to(np.array([-6, 2.5, 0])).to_edge(LEFT)
        origin_location = Text('(x=0 z=0)', font_size=25).move_to(np.array([-4.1, 3.0, 0]))
        symbol_group = VGroup(circle_symbol, symbol_text)
        origin_group = VGroup(origin_symbol, origin_text)
        radius_group = VGroup()
        annulus_weight_group = VGroup()
        stronghold_counts = VGroup(
            Text('3', font='Source Han Sans HC ExtraLight', font_size=20, color=ORANGE),
            Text('6', font='Source Han Sans HC ExtraLight', font_size=20, color=ORANGE),
            Text('10', font='Source Han Sans HC ExtraLight', font_size=20, color=ORANGE),
            Text('15', font='Source Han Sans HC ExtraLight', font_size=20, color=ORANGE),
            Text('21', font='Source Han Sans HC ExtraLight', font_size=20, color=ORANGE),
            Text('28', font='Source Han Sans HC ExtraLight', font_size=20, color=ORANGE),
            Text('36', font='Source Han Sans HC ExtraLight', font_size=20, color=ORANGE),
            Text('9', font='Source Han Sans HC ExtraLight', font_size=20, color=ORANGE),
        )
        for step in range(0, 8):
            inner_radius = 1280 + 1536 * step * 2
            outer_radius = 1280 + 1536 * (step * 2 + 1)
            inner_weight = -0.04 + (0.48 * (step + 1))
            outer_weight = -0.28 + (0.48 * (step + 1))
            middle = -0.16 + (0.48 * (step + 1))
            inner_line = Line(start=np.array([0, -inner_weight, 0]), end=np.array([0.2, -middle, 0]),
                              stroke_width=1, color=BLUE_D)
            outer_line = Line(start=np.array([0, -outer_weight, 0]), end=np.array([0.2, -middle, 0]),
                              stroke_width=1, color=BLUE_D)
            annulus_weight = Text('1536', font='Source Han Sans HC ExtraLight', font_size=20, color=BLUE_D
                                  ).move_to(np.array([0.5, -middle, 0]))
            radius_group.add(Text(str(inner_radius) + ' ~ ' + str(outer_radius), font='Source Han Sans HC ExtraLight',
                                  font_size=18, color=TEAL).move_to(np.array([0.8, -0.16 + (0.48 * (step + 1)), 0])))
            annulus_weight_group.add(inner_line, outer_line, annulus_weight)
            stronghold_counts[step].move_to(np.array([0.3, -middle, 0]))
        self.wait()
        self.play(
            LaggedStart(*[GrowFromCenter(obj) for obj in circle_group_uneffect], run_time=1.5),
        )
        self.play(FadeIn(stroke_group_uneffect))
        self.play(
            LaggedStart(*[ShowCreationThenDestruction(
                circle_group_uneffect[i].copy().set_color(YELLOW_D).rotate(angle=-i * (90 / 7) * DEGREES))
                for i in range(0, 8)], run_time=5),
            FadeIn(symbol_group),
            rate_func=smooth
        )
        self.wait()
        self.play(
            GrowFromCenter(origin_point),
            FadeIn(origin_group),
            rate_func=smooth
        )
        self.wait()
        self.play(FadeInFromPoint(origin_location, origin_symbol.get_center(), run_time=0.5, rate_func=smooth))
        self.wait()
        self.remove(circle_group_uneffect, stroke_group_uneffect).add(circle_group, stroke_group).play(
            path.animate.set_value(180),
            LaggedStart(*[FadeInFromPoint(radius_group[7 - i], radius_group[7 - i].get_left())
                          for i in range(0, 8)], run_time=1),
            FadeIn(radius_text),
            rate_func=smooth
        )
        self.wait()
        self.play(
            LaggedStart(*[FadeInFromPoint(obj, obj.get_left())
                          for obj in annulus_weight_group], run_time=1, rate_func=smooth)
        )
        self.wait()

        self.play(
            LaggedStart(
                ReplacementTransform(annulus_weight_group[2], stronghold_counts[0]),
                ReplacementTransform(annulus_weight_group[5], stronghold_counts[1]),
                ReplacementTransform(annulus_weight_group[8], stronghold_counts[2]),
                ReplacementTransform(annulus_weight_group[11], stronghold_counts[3]),
                ReplacementTransform(annulus_weight_group[14], stronghold_counts[4]),
                ReplacementTransform(annulus_weight_group[17], stronghold_counts[5]),
                ReplacementTransform(annulus_weight_group[20], stronghold_counts[6]),
                ReplacementTransform(annulus_weight_group[23], stronghold_counts[7]),
                run_time=1,
            ),
            FadeOut(annulus_weight_group[0:2]),
            FadeOut(annulus_weight_group[3:5]),
            FadeOut(annulus_weight_group[6:8]),
            FadeOut(annulus_weight_group[9:11]),
            FadeOut(annulus_weight_group[12:14]),
            FadeOut(annulus_weight_group[15:17]),
            FadeOut(annulus_weight_group[18:20]),
            FadeOut(annulus_weight_group[21:23]),
            rate_func=smooth
        )
        self.wait()

        rate = 1.3
        arc_1280 = Arc(radius=1.280 * rate, angle=TAU, color=BLUE_D, stroke_width=3, arc_center=ORIGIN)
        arc_2816 = Arc(radius=2.816 * rate, angle=TAU, color=BLUE_D, stroke_width=3, arc_center=ORIGIN)
        annulus_fill = Circle(radius=2.048 * rate, stroke_width=153.6 * rate, stroke_opacity=0.5, color='#8eba89')
        self.play(
            FadeOut(radius_text),
            FadeOut(stronghold_counts),
            FadeOut(radius_group),
            FadeOut(circle_group[1:]),
            FadeOut(stroke_group[2:]),
            ReplacementTransform(stroke_group[1], arc_1280),
            ReplacementTransform(stroke_group[0], arc_2816),
            ReplacementTransform(circle_group[0], annulus_fill),
            run_time=1,
            rate_func=smooth
        )
        self.wait()


class Scene10(Scene):  # 281
    def waiting(self, second=0, frame=0, fps=60):
        self.wait(second + frame / fps)

    def construct(self):
        background = ImageMobject('assets\\raster_images\\back4.png', height=8)
        background.add_updater(lambda bg: self.bring_to_back(bg))
        axes = Axes(
            x_range=(0, 2200),
            y_range=(0, 2000),
            height=6.3,
            width=12,
            axis_config={
                "include_tip": True,
                "include_ticks": False,
                "include_numbers": False
            }
        )
        axe_x_text = Tex(r'\mathtt{{x}}').move_to(axes.c2p(2175, 125))
        axe_y_text = Tex(r'\mathtt{{y}}').move_to(axes.c2p(65, 2000))
        ave = axes.get_graph(
            lambda x: 2E-7 * x ** 3 - 6E-4 * x ** 2 - 0.0837 * x + 1727.7,
            color=BLUE,
            x_range=(0, 2100, 100)
        )
        highroll = axes.get_graph(
            lambda x: 2E-7 * x ** 3 - 5E-4 * x ** 2 - 0.4192 * x + 1482.1,
            color=GREEN,
            x_range=(0, 2100, 100)
        )
        y_1728 = Text('1728', font_size=23, color=BLUE).move_to(axes.c2p(0, 1727.7)).shift(LEFT * 0.4)
        y_1482 = Text('1482', font_size=23, color=GREEN).move_to(axes.c2p(0, 1482)).shift(LEFT * 0.4)
        y_500 = Text('500', font_size=23).move_to(axes.c2p(0, 500)).shift(LEFT * 0.3)
        y_1000 = Text('1000', font_size=23).move_to(axes.c2p(0, 1000)).shift(LEFT * 0.4)
        x_500 = Text('500', font_size=23).move_to(axes.c2p(500, 0)).shift(DOWN * 0.2)
        x_1000 = Text('1000', font_size=23).move_to(axes.c2p(1000, 0)).shift(DOWN * 0.2)
        x_1500 = Text('1500', font_size=23).move_to(axes.c2p(1500, 0)).shift(DOWN * 0.2)
        x_2000 = Text('2000', font_size=23).move_to(axes.c2p(2000, 0)).shift(DOWN * 0.2)
        axes_0 = Text('0', font_size=23).move_to(axes.c2p(0, 0)).shift(DOWN * 0.2)
        fx_text = Text('平均情况', font='Source Han Sans HC Normal', font_size=30
                       ).next_to(ave).to_corner(UR).shift(DOWN * 1.7)
        fx_symbol = Line(start=fx_text.copy().shift(LEFT * 0.7).get_left(),
                         end=fx_text.copy().shift(LEFT * 0.2).get_left(), color=BLUE)
        fx_keys = VGroup(fx_text, fx_symbol)
        gx_text = Text('最佳情况', font='Source Han Sans HC Normal', font_size=30
                       ).next_to(ave).to_corner(UR).shift(DOWN * 2.3)
        gx_symbol = Line(start=gx_text.copy().shift(LEFT * 0.7).get_left(),
                         end=gx_text.copy().shift(LEFT * 0.2).get_left(), color=GREEN)
        gx_keys = VGroup(gx_text, gx_symbol)
        anims = [Write(axes), FadeIn(axe_x_text), FadeIn(axe_y_text), Write(axes_0), Write(y_1728), Write(y_1482),
                 Write(y_500), Write(y_1000), Write(x_500), Write(x_1000), Write(x_1500), Write(x_2000), ]
        self.wait()
        self.play(
            LaggedStart(*anims, run_time=1, rate_func=smooth),
            LaggedStart(*[Write(ave), Write(highroll), ], run_time=2, rate_func=smooth),
        )
        self.wait()

        x_text = Text('与 世 界 原 点 的 距 离', font='Source Han Sans HC Light', font_size=30, color='#ee6363'
                      ).move_to(np.array([-3.7, -2.8, 0]))
        y_text = Text('与 最 近 要 塞 的 距 离', font='Source Han Sans HC Light', font_size=30, color='#52a36e'
                      ).rotate(angle=90 * DEGREES).move_to(np.array([-5.65, -0.75, 0]))
        bed = ImageMobject('assets\\raster_images\\bed2.webp', height=1).move_to(axes.get_x_axis().get_end())
        strh = ImageMobject('assets\\raster_images\\PortalRoom.webp', height=1).move_to(axes.get_y_axis().get_end())
        x_axe = axes.get_x_axis().copy()
        y_axe = axes.get_y_axis().copy()
        axe_x_text.add_updater(lambda obj: self.bring_to_front(obj))
        axe_y_text.add_updater(lambda obj: self.bring_to_front(obj))
        axes.add_updater(lambda obj: self.bring_to_front(obj))
        x_axe.add_updater(lambda obj: self.bring_to_front(obj))
        y_axe.add_updater(lambda obj: self.bring_to_front(obj))
        self.play(
            Write(x_text, run_time=0.5),
            GrowFromCenter(bed, run_time=0.5),
            rate_func=smooth
        )
        self.wait()
        self.play(
            Write(y_text, run_time=0.5),
            GrowFromCenter(strh, run_time=0.5),
            rate_func=smooth
        )
        self.bring_to_back(bed, strh).wait()
        self.play(
            ShowCreationThenDestruction(ave.copy().set_color(YELLOW)),
            ShowCreation(fx_symbol, run_time=0.5),
            Write(fx_text),
            rate_func=smooth
        )
        self.wait()
        self.play(
            ShowCreationThenDestruction(highroll.copy().set_color(YELLOW)),
            ShowCreation(gx_symbol, run_time=0.5),
            Write(gx_text),
            rate_func=smooth
        )
        self.wait()

        axe_x_text.clear_updaters()
        axe_y_text.clear_updaters()
        axes.clear_updaters()
        x_axe.clear_updaters()
        y_axe.clear_updaters()
        ave_run_dot = Dot(radius=0.07, color=YELLOW)
        ave_run_dot.move_to(axes.i2gp(0, ave))
        ave_x_tracker = ValueTracker(0)
        f_always(ave_run_dot.move_to, lambda: axes.i2gp(ave_x_tracker.get_value(), ave))
        ave_h_line = always_redraw(lambda: axes.get_h_line(ave_run_dot.get_left()))
        ave_v_line = always_redraw(lambda: axes.get_v_line(ave_run_dot.get_bottom()))
        ave_run_dot_x_text = Integer(
            show_ellipsis=False,
            num_decimal_places=0,
            include_sign=False,
            group_with_commas=False,
            font_size=23,
        ).add_updater(
            lambda obj: obj.set_value(
                ave_x_tracker.get_value()).set_color(YELLOW_D).move_to(ave_v_line.get_bottom()).shift(DOWN * 0.2))
        ave_run_dot_y_text = Integer(
            show_ellipsis=False,
            num_decimal_places=0,
            include_sign=False,
            group_with_commas=False,
            font_size=23,
        )
        ave_run_dot_y_text_in = ave_run_dot_y_text.copy().add_updater(
            lambda obj: obj.set_value(
                2E-7 * ave_x_tracker.get_value() ** 3 - 6E-4 * ave_x_tracker.get_value() ** 2
                - 0.0837 * ave_x_tracker.get_value() + 1727.7).set_color(YELLOW_D).move_to(
                ave_run_dot.get_center()).shift(LEFT * 0.4))
        ave_run_dot_y_text.add_updater(
            lambda obj: obj.set_value(
                2E-7 * ave_x_tracker.get_value() ** 3 - 6E-4 * ave_x_tracker.get_value() ** 2
                - 0.0837 * ave_x_tracker.get_value() + 1727.7).set_color(YELLOW_D).move_to(
                ave_h_line.get_left()).shift(LEFT * 0.36))
        highroll_run_dot = Dot(radius=0.07, color=YELLOW)
        highroll_run_dot.move_to(axes.i2gp(0, highroll))
        highroll_x_tracker = ValueTracker(0)
        f_always(highroll_run_dot.move_to, lambda: axes.i2gp(highroll_x_tracker.get_value(), highroll))
        highroll_h_line = always_redraw(lambda: axes.get_h_line(highroll_run_dot.get_left()))
        highroll_v_line = always_redraw(lambda: axes.get_v_line(highroll_run_dot.get_bottom()))
        highroll_run_dot_x_text = Integer(
            show_ellipsis=False,
            num_decimal_places=0,
            include_sign=False,
            group_with_commas=False,
            font_size=23,
        ).add_updater(
            lambda obj: obj.set_value(
                highroll_x_tracker.get_value()).set_color(YELLOW_D).move_to(
                highroll_v_line.get_bottom()).shift(DOWN * 0.2))
        highroll_run_dot_y_text = Integer(
            show_ellipsis=False,
            num_decimal_places=0,
            include_sign=False,
            group_with_commas=False,
            font_size=23,
        )
        highroll_run_dot_y_text_in = highroll_run_dot_y_text.copy().add_updater(
            lambda obj: obj.set_value(
                2E-7 * highroll_x_tracker.get_value() ** 3 - 5E-4 * highroll_x_tracker.get_value() ** 2 - 0.4192
                * highroll_x_tracker.get_value() + 1482.1).set_color(YELLOW_D).move_to(
                highroll_run_dot.get_center()).shift(LEFT * 0.4))
        highroll_run_dot_y_text.add_updater(
            lambda obj: obj.set_value(
                2E-7 * highroll_x_tracker.get_value() ** 3 - 5E-4 * highroll_x_tracker.get_value() ** 2 - 0.4192
                * highroll_x_tracker.get_value() + 1482.1).set_color(YELLOW_D).move_to(
                highroll_h_line.get_left()).shift(LEFT * 0.36))
        self.play(
            GrowFromCenter(ave_run_dot),
            FadeOut(x_text),
            FadeOut(y_text),
            FadeIn(ave_h_line),
            FadeIn(ave_v_line),
            FadeIn(ave_run_dot_x_text),
            FadeIn(ave_run_dot_y_text_in),
            highroll.animate.set_stroke(opacity=0.3),
            gx_keys.animate.set_opacity(0.3)
        )
        self.remove(ave_run_dot_y_text_in).add(ave_run_dot_y_text)
        self.play(ave_x_tracker.animate.set_value(1700), run_time=1.5, rate_func=smooth)
        self.wait()
        self.play(
            AnimationGroup(
                Indicate(ave_run_dot_x_text),
                ShowCreationThenDestruction(
                    Line(start=ave_v_line.get_bottom(), end=ave_v_line.get_top(), color=YELLOW)),
            ),
            rate_func=smooth
        )
        self.wait()
        self.play(
            AnimationGroup(
                ShowCreationThenDestruction(
                    Line(start=ave_h_line.get_right(), end=ave_h_line.get_left(), color=YELLOW)),
                Indicate(ave_run_dot_y_text),
                lag_ratio=0.4
            ),
            rate_func=smooth
        )
        self.wait()
        self.play(
            FadeOut(ave_run_dot_x_text),
            FadeOut(ave_run_dot_y_text),
            FadeOut(ave_run_dot),
            FadeOut(ave_h_line),
            FadeOut(ave_v_line),
            highroll.animate.set_stroke(opacity=1),
            gx_keys.animate.set_opacity(1),
            GrowFromCenter(highroll_run_dot),
            FadeIn(highroll_h_line),
            FadeIn(highroll_v_line),
            FadeIn(highroll_run_dot_x_text),
            FadeIn(highroll_run_dot_y_text_in),
            ave.animate.set_stroke(opacity=0.3),
            fx_keys.animate.set_opacity(0.3)
        )
        self.remove(highroll_run_dot_y_text_in).add(highroll_run_dot_y_text)
        self.play(highroll_x_tracker.animate.set_value(1800), run_time=1.5, rate_func=smooth)
        self.wait()
        self.play(
            AnimationGroup(
                Indicate(highroll_run_dot_x_text),
                ShowCreationThenDestruction(
                    Line(start=highroll_v_line.get_bottom(), end=highroll_v_line.get_top(), color=YELLOW)),
                lag_ratio=0.4
            ),
            rate_func=smooth
        )
        self.wait()
        self.play(
            AnimationGroup(
                ShowCreationThenDestruction(
                    Line(start=highroll_h_line.get_right(), end=highroll_h_line.get_left(), color=YELLOW)),
                Indicate(highroll_run_dot_y_text),
                lag_ratio=0.4
            ),
            rate_func=smooth
        )
        self.wait()

        ave_1728_h_line = axes.get_h_line(axes.i2gp(1728, ave))
        ave_1728_v_line = axes.get_v_line(axes.i2gp(1728, ave))
        ave_1728_dot_y_text = Integer(
            show_ellipsis=False,
            num_decimal_places=0,
            include_sign=False,
            group_with_commas=False,
            font_size=23,
        ).add_updater(
            lambda obj: obj.set_value(2E-7 * 1728 ** 3 - 6E-4 * 1728 ** 2 - 0.0837 * 1728 + 1727.7
                                      ).set_color(YELLOW_D).move_to(ave_1728_h_line.get_left()).shift(LEFT * 0.36))
        highroll_run_dot.add_updater(lambda obj: self.bring_to_front(obj))
        self.play(
            AnimationGroup(
                AnimationGroup(
                    ave.animate.set_stroke(opacity=1),
                    fx_keys.animate.set_opacity(1),
                    highroll_x_tracker.animate.set_value(1728),
                ),
                AnimationGroup(
                    FadeIn(ave_1728_h_line),
                    FadeIn(ave_1728_v_line),
                    FadeIn(ave_1728_dot_y_text),
                    GrowFromCenter(Dot(radius=0.07, color=YELLOW).move_to(axes.i2gp(1728, ave)))
                ),
                lag_ratio=0.5
            )
        )
        self.play(
            LaggedStart(
                Indicate(highroll_run_dot_x_text),
                ShowCreationThenDestruction(
                    Line(start=ave_1728_v_line.get_bottom(), end=ave_1728_v_line.get_top(), color=YELLOW)),
                ShowCreationThenDestruction(
                    Line(start=highroll_h_line.get_right(), end=highroll_h_line.get_left(), color=YELLOW)),
                AnimationGroup(
                    Indicate(highroll_run_dot_y_text),
                    ShowCreationThenDestruction(
                        Line(start=ave_1728_h_line.get_right(), end=ave_1728_h_line.get_left(), color=YELLOW)),
                ),
                Indicate(ave_1728_dot_y_text),
                lag_ratio=0.2,
                run_time=2,
                rate_func=smooth
            )
        )
        self.wait()

        highroll_run_dot_x_text.clear_updaters()
        self.play(
            ShowCreationThenDestruction(Line(start=axes.c2p(0, 0), end=axes.c2p(1728, 0), color=RED)),
            highroll_run_dot_x_text.animate.set_color(color=RED),
            rate_func=smooth
        )
        self.wait()
