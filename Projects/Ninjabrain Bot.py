from manimlib import *


# 该函数来自Manim Kindergarten Sandbox
def debug(self, tex, scale_factor=0.6, text_color=PURPLE):
    for i, j in enumerate(tex):
        tex_id = Text(str(i), font="Consolas").scale(scale_factor).set_color(text_color)
        tex_id.move_to(j)
        self.add(tex_id)


def arc_text(text, radius, angle, arc_buff):
    nums = len(text)
    for i in range(nums):
        text[i].move_to(radius * UP).rotate(- i * (angle / (nums - 1)) * DEGREES, about_point=ORIGIN)
    text.rotate((angle / 2) * DEGREES, about_point=ORIGIN)
    arc = Arc(radius=radius, start_angle=(90 + angle / 2 + arc_buff) * DEGREES,
              angle=TAU - (angle * DEGREES + 2 * arc_buff * DEGREES), arc_center=ORIGIN)
    return arc


def cords_generator(px, py, t1, t2, r1, r2, dots):
    target_temp = []
    not_target_temp = []
    for item in dots:
        pos_x, pos_y = item.get_center()[0], item.get_center()[1]
        by = (t1 * (pos_x - px)) + py
        uy = (t2 * (pos_x - px)) + py
        lx = ((pos_y - py) / t2) + px
        rx = ((pos_y - py) / t1) + px
        if by < pos_y < uy and lx < pos_x < rx and r1 <= np.sqrt(pos_x ** 2 + pos_y ** 2) <= r2:
            target_temp.append((pos_x, pos_y))
        else:
            not_target_temp.append((pos_x, pos_y))
    return target_temp, not_target_temp


########################################################################################################################
class Scene1(Scene):  # 50
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
        cp_main = line_intersection(
            line_left.get_start_and_end(),
            line_right.get_start_and_end()
        )
        cross_point = Dot(point=cp_main, radius=0.07, color=RED_D)
        eye_image_left = ImageMobject(
            r'assets\raster_images\Eye.webp', height=0.6).next_to(eye_left, LEFT).shift(RIGHT * 0.1)
        eye_image_right = ImageMobject(
            r'assets\raster_images\Eye.webp', height=0.6).next_to(eye_right).shift(LEFT * 0.1)
        player_image_left = ImageMobject(
            r'assets\raster_images\HumanFace.webp', height=0.4).next_to(player_left, LEFT)
        player_image_right = ImageMobject(
            r'assets\raster_images\HumanFace.webp', height=0.4
        ).next_to(player_right).shift(UP * 0.25 + LEFT * 0.1)
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
        bg.clear_updaters()
        self.play(
            FadeIn(cross_point, run_time=1),
            self.camera.frame.animate.scale(0.75).move_to(cross_point).shift(DOWN * 0.5),
            bg.animate.scale(0.75).move_to(cross_point),
            rate_func=smooth
        )
        self.wait()


class Scene2(Scene):  # 253
    def construct(self):
        axes = Axes(
            x_range=(-960, 960),
            y_range=(-540, 540),
            height=9,
            width=16,
            axis_config={"include_tip": True, "include_ticks": False},
        ).move_to(ORIGIN)
        coord_group = [(x, y) for y in range(-540, 540) for x in range(-960, 960) if
                       ((x - 12) / 24) % 1 == 0 and ((y - 12) / 24) % 1 == 0]
        dot_group = VGroup(*[Dot(point=axes.c2p(item[0], item[1]), radius=0.007, color=GREY_C) for item in coord_group])
        vertical_dots = VGroup()
        temp = VGroup()
        for idx in range(0, len(dot_group)):
            if dot_group[idx].get_center()[1] == dot_group[idx - 1].get_center()[1]:
                temp.add(dot_group[idx])
            else:
                temp = VGroup(dot_group[idx])
            vertical_dots.add(temp)
        rate = 1.3
        text_1280 = Text('R=1280', font='Source Han Sans HC Light', font_size=18, color=BLUE_B)
        text_2816 = Text('R=2816', font='Source Han Sans HC Light', font_size=18, color=BLUE_B)
        arc_text_1280 = arc_text(text=text_1280, radius=1.28 * rate, angle=30, arc_buff=5
                                 ).set_color(color=BLUE_D).set_style(stroke_width=1)
        arc_text_2816 = arc_text(text=text_2816, radius=2.816 * rate, angle=20, arc_buff=2
                                 ).set_color(color=BLUE_D).set_style(stroke_width=1)
        annulus_fill = Circle(radius=2.048 * rate, stroke_width=153.6 * rate, stroke_opacity=0.5, color=BLUE_D)
        origin = Dot(point=ORIGIN, radius=0.05, color="#70AD47")

        # 参数定义
        player_x, player_y = 50, -120
        cle_x, cle_y = 1034, 1100
        fov_x = 1000
        sigma = 7.3
        player = Dot(point=axes.c2p(player_x, player_y), radius=0.05, color="#8C3FC5")
        # 构建中心直线
        central_line = Line(start=player.get_center(), end=axes.c2p(cle_x, cle_y), stroke_width=2.5, color="#E73750")
        # 获取中心直线的倾斜角并计算视野上下界的倾斜角
        theta_1 = central_line.get_angle() - (sigma * DEGREES)
        theta_2 = central_line.get_angle() + (sigma * DEGREES)
        # 根据给定的视野上下界x轴坐标计算y轴坐标
        fov1_y = (np.tan(theta_1) * (fov_x - player_x)) + player_y
        fov2_y = (np.tan(theta_2) * (fov_x - player_x)) + player_y
        # 构建视野上下界
        fov1_l = DashedLine(start=player.get_center(), end=axes.c2p(fov_x, fov1_y), stroke_width=1.5, color="#8B8B8B",
                            dash_length=0.2).set_opacity(0.7)
        fov2_l = DashedLine(start=player.get_center(), end=axes.c2p(fov_x, fov2_y), stroke_width=1.5, color="#8B8B8B",
                            dash_length=0.2).set_opacity(0.7)
        # 获取候选要塞坐标集合
        target_list, not_target_list = cords_generator(
            player.get_center()[0], player.get_center()[1], fov1_l.get_slope(), fov2_l.get_slope(),
            1.28 * rate, 2.816 * rate, dot_group)
        # 构建候选要塞点集合
        target_dot_group = VGroup(
            *[Dot(point=np.array((item[0], item[1], 0)), radius=0.02, color=YELLOW_D) for item in target_list])
        not_target_dot_group = VGroup(
            *[Dot(point=np.array((item[0], item[1], 0)), radius=0.007, color=GREY_C) for item in not_target_list])
        print(len(target_dot_group))

        self.play(
            LaggedStart(
                *[FadeIn(vertical_dots[-anim]) for anim in range(-len(vertical_dots) + 1, 1)],
                run_time=1.5,
                lag_ratio=0.1,
                rate_func=rush_from)
        )
        self.wait()
        self.play(
            ShowCreation(arc_text_1280),
            ShowCreation(arc_text_2816),
            ShowCreation(axes),
            FadeIn(annulus_fill),
            Write(text_1280),
            Write(text_2816),
            ShowCreation(central_line),
            GrowFromCenter(origin),
            GrowFromCenter(player),
            rate_func=smooth
        )
        self.wait()
        player.add_updater(lambda obj: self.bring_to_front(obj))
        self.play(
            ShowCreation(fov1_l),
            ShowCreation(fov2_l),
            rate_func=smooth
        )
        self.wait()
        self.play(
            self.camera.frame.animate.scale(0.5).move_to([2, 1.3, 0]),
            LaggedStart(
                *[GrowFromCenter(target_dot_group[anim]) for anim in range(0, len(target_dot_group))],
                run_time=1,
                lag_ratio=0.1,
                rate_func=rush_from
            ),
            rate_func=smooth
        )
        final = target_dot_group[20].copy().set_color(RED).scale(2)
        self.wait()
        self.remove(dot_group).add(not_target_dot_group).bring_to_back(not_target_dot_group)
        target_dot_group_trans = VGroup(*[Dot(radius=0.05, color=YELLOW_D) for _ in range(len(target_dot_group))])
        target_dot_group_trans.arrange_in_grid(n_rows=5, n_cols=8, v_buff=0.3, h_buff=0.5).move_to([2, 0.8, 0])
        mask = Rectangle(
            height=9, width=16).set_fill(color=BLACK, opacity=0.85).set_stroke(opacity=0).move_to([2, 1.3, 0])
        frame = Rectangle(height=10, width=23.5).set_fill(color=BLUE, opacity=0).set_stroke(
            width=2.5, color=WHITE).scale(0.2).move_to(target_dot_group_trans.get_center())
        frame_g = Rectangle(height=8.5, width=8.5).set_fill(color=BLUE, opacity=0).set_stroke(
            width=2.5, color=WHITE).scale(0.2).move_to(target_dot_group_trans.get_center())
        g = Text('G', font='GlowSansSC-Normal-Light', font_size=75, t2c={'G': YELLOW_D}).move_to(
            target_dot_group_trans.get_center())
        target_dot_group_old = target_dot_group.copy()
        self.remove(target_dot_group).add(target_dot_group_old)
        self.play(
            FadeIn(mask),
            ShowCreation(frame),
            LaggedStart(
                *[ReplacementTransform(
                    target_dot_group_old[idx], target_dot_group_trans[len(target_dot_group) - idx - 1]
                ) for idx in range(0, len(target_dot_group))],
                run_time=1.5,
                lag_ratio=0.1,
                rate_func=rush_from
            ),
            run_time=1.5,
            rate_func=smooth
        )
        self.wait()
        self.play(
            ReplacementTransform(target_dot_group_trans, g),
            ReplacementTransform(frame, frame_g),
            run_time=1,
            rate_func=smooth
        )
        self.wait()
        set_g = VGroup(g.copy(), frame.copy())
        self.remove(g).remove(frame_g).add(set_g)
        self.play(
            FadeOut(mask),
            set_g.animate.scale(0.5).shift(RIGHT * 2.5 + UP * 0.7),
            self.camera.frame.animate.scale(0.8).move_to(final.get_center()),
            run_time=1.5,
            rate_func=smooth
        )
        self.play(
            FadeInFromPoint(final, set_g.get_center()),
            run_time=1,
            rate_func=smooth
        )
        self.wait()
        self.play(
            LaggedStart(
                *[FadeInFromPoint(target_dot_group[idx], set_g.get_center()) for idx in range(0, 20)],
                ReplacementTransform(final, target_dot_group[20]),
                *[FadeInFromPoint(target_dot_group[idx], set_g.get_center()) for idx in range(21, len(target_dot_group))],
                run_time=1,
                lag_ratio=0.1,
                rate_func=rush_from
            )
        )
        self.wait()
        # 构建第二个视野
        player_x_2, player_y_2 = 70, 80
        cle_x_2, cle_y_2 = 800, 340
        fov_x_2 = 700
        player_2 = Dot(point=axes.c2p(player_x_2, player_y_2), radius=0.05, color="#8C3FC5")
        # 构建中心直线
        central_line_2 = Line(
            start=player_2.get_center(), end=axes.c2p(cle_x_2, cle_y_2), stroke_width=2.5, color="#E73750")
        # 获取中心直线的倾斜角并计算视野上下界的倾斜角
        theta_1_2 = central_line_2.get_angle() - (sigma * DEGREES)
        theta_2_2 = central_line_2.get_angle() + (sigma * DEGREES)
        # 根据给定的视野上下界x轴坐标计算y轴坐标
        fov1_y_2 = (np.tan(theta_1_2) * (fov_x_2 - player_x_2)) + player_y_2
        fov2_y_2 = (np.tan(theta_2_2) * (fov_x_2 - player_x_2)) + player_y_2
        # 构建视野上下界
        fov1_l_2 = DashedLine(start=player_2.get_center(), end=axes.c2p(fov_x_2, fov1_y_2),
                              stroke_width=1.5, color="#8B8B8B", dash_length=0.2).set_opacity(0.7)
        fov2_l_2 = DashedLine(start=player_2.get_center(), end=axes.c2p(fov_x_2, fov2_y_2),
                              stroke_width=1.5, color="#8B8B8B", dash_length=0.2).set_opacity(0.7)
        # 获取候选要塞坐标集合
        target_list_2, not_target_list_2 = cords_generator(
            player_2.get_center()[0], player_2.get_center()[1], fov1_l_2.get_slope(), fov2_l_2.get_slope(),
            1.28 * rate, 2.816 * rate, dot_group)
        # 构建候选要塞点集合
        target_dot_group_2 = VGroup(
            *[Dot(point=np.array((item[0], item[1], 0)), radius=0.02, color=YELLOW_D) for item in target_list_2])
        not_target_dot_group_2 = VGroup(
            *[Dot(point=np.array((item[0], item[1], 0)), radius=0.007, color=GREY_C) for item in not_target_list_2])
        print(len(target_dot_group_2))
        self.play(
            GrowFromCenter(player_2),
            run_time=1,
            rate_func=smooth,
        )
        player_2.add_updater(lambda obj: self.bring_to_front(obj))
        self.play(
            self.camera.frame.animate.scale(1.4).shift(LEFT * 0.9 + DOWN * 0.9),
            set_g.animate.shift(RIGHT * 0.3 + DOWN * 0.8),
            *[ShowCreation(item) for item in [central_line_2, fov1_l_2, fov2_l_2]],
            LaggedStart(
                *[GrowFromCenter(target_dot_group_2[anim]) for anim in range(0, len(target_dot_group_2))],
                run_time=1,
                lag_ratio=0.1,
                rate_func=rush_from
            ),
            run_time=1,
            rate_func=smooth,
        )
        self.wait()
        set_g.add_updater(lambda obj: self.bring_to_front(obj))
        # 计算候选要塞集合
        temp_1 = [item for item in target_dot_group]
        temp_2 = [item for item in target_dot_group_2]
        target_dot_group_union = VGroup(*[item for item in list(set(temp_1).union(set(temp_2)))])
        # 计算非候选要塞集合
        temp_3 = [(item.get_center()[0], item.get_center()[1]) for item in dot_group]
        temp_4 = [(item.get_center()[0], item.get_center()[1]) for item in not_target_dot_group]
        temp_5 = [(item.get_center()[0], item.get_center()[1]) for item in not_target_dot_group_2]
        not_target_dot_group_all = VGroup(*[Dot(point=np.array((item[0], item[1], 0)), radius=0.007, color=GREY_C) for item in temp_3 if item in temp_4 and item in temp_5])
        self.remove(not_target_dot_group).remove(target_dot_group_2).add(not_target_dot_group_all, target_dot_group_union, set_g)
        self.play(
            LaggedStart(
                *[FadeOutToPoint(target_dot_group_union[anim], set_g[1].get_center()) for anim in range(0, len(target_dot_group_union))],
                run_time=1.5,
                lag_ratio=0.1,
                rate_func=rush_from
            ),
            Indicate(set_g[1], run_time=1.5),
        )
        self.wait()
        p1_fov1_indicate = DashedLine(start=player.get_center(), end=axes.c2p(fov_x, fov1_y), stroke_width=1.5, color=YELLOW_D, dash_length=0.2)
        p1_fov2_indicate = DashedLine(start=player.get_center(), end=axes.c2p(fov_x, fov2_y), stroke_width=1.5, color=YELLOW_D, dash_length=0.2)
        p2_fov1_indicate = DashedLine(start=player_2.get_center(), end=axes.c2p(fov_x_2, fov1_y_2), stroke_width=1.5, color=YELLOW_D, dash_length=0.2)
        p2_fov2_indicate = DashedLine(start=player_2.get_center(), end=axes.c2p(fov_x_2, fov2_y_2), stroke_width=1.5, color=YELLOW_D, dash_length=0.2)
        self.play(
            *[ShowCreationThenDestruction(item) for item in [p1_fov1_indicate, p1_fov2_indicate, p2_fov1_indicate, p2_fov2_indicate]],
            run_time=1,
            rate_func=smooth
        )
        self.wait()
        set_g.clear_updaters()
        player.clear_updaters()
        player_2.clear_updaters()
        p1 = VGroup(fov1_l, fov2_l, central_line, player)
        self.play(
            *[FadeOut(item) for item in [not_target_dot_group_all, axes, origin, player_2, central_line_2, fov1_l_2, fov2_l_2, set_g, arc_text_1280, arc_text_2816, text_1280, text_2816, annulus_fill]],
            Rotating(p1, angle=np.arctan(-np.tan(central_line.get_angle())), about_point=player.get_center(), run_time=0.6),
            self.camera.frame.animate.scale(0.5).shift(RIGHT * 5 + DOWN * 1.65),
            run_time=2,
            rate_func=smooth
        )
        self.wait()


class Scene3(Scene):  # 20
    def construct(self):
        axes = Axes(
            x_range=(-5, 5),
            y_range=(0, 0.25),
            height=6.3,
            width=12,
            axis_config={
                "include_tip": True,
                "include_ticks": False,
                "include_numbers": False
            }
        )
        ave = axes.get_graph(
            lambda x: np.exp(-(x ** 2 / 2)) / (np.sqrt(2) * np.pi),
            color=BLUE,
            x_range=(-5, 5, 0.1)
        )
        self.play(
            ShowCreation(ave),
        )


class Scene4(Scene):  # 235
    def construct(self):
        gird = NumberPlane(
            faded_line_ratio=0,
            background_line_style={
                "stroke_opacity": 0.5,
                "stroke_color": GREY
            }
        )
        text_origin = Text('世界原点', font='Source Han Sans HC Light', font_size=22)
        text_player = Text('玩家位置', font='Source Han Sans HC Light', font_size=22)
        text_str = Text('实际要塞', font='Source Han Sans HC Light', font_size=22)
        text_c_str = Text('候选要塞', font='Source Han Sans HC Light', font_size=22)
        key_origin = Dot(radius=0.12, color="#70AD47")
        key_player = Dot(radius=0.12, color="#8C3FC5")
        key_str = Dot(radius=0.12, color=RED_E)
        key_c_str = Dot(radius=0.12, color=YELLOW_D)
        keys_and_texts_1 = VGroup(
            key_origin.copy(), text_origin.copy(),
            key_player.copy(), text_player.copy(),
            key_str.copy(), text_str.copy()
        ).arrange_in_grid(
            n_rows=3, n_cols=2, v_buff=0.3, h_buff=0
        ).add_background_rectangle(
            color="#181717", buff=0.2, stroke_width=5, stroke_color=BLACK, stroke_opacity=1, opacity=1
        ).scale(0.6).to_corner(LEFT + UP).shift(LEFT * 0.3 + UP * 0.3)
        keys_and_texts_2 = VGroup(
            key_origin.copy(), text_origin.copy(),
            key_player.copy(), text_player.copy(),
            key_str.copy(), text_str.copy(),
            key_c_str.copy(), text_c_str.copy()
        ).arrange_in_grid(
            n_rows=4, n_cols=2, v_buff=0.3, h_buff=0
        ).add_background_rectangle(
            color="#181717", buff=0.2, stroke_width=5, stroke_color=BLACK, stroke_opacity=1, opacity=1
        ).scale(0.6).to_corner(LEFT + UP).shift(LEFT * 0.3 + UP * 0.325)
        rate = 1.3
        arc_1280 = Circle(radius=1.28 * rate).set_color(color=BLUE_D).set_style(stroke_width=1)
        arc_2816 = Circle(radius=2.816 * rate).set_color(color=BLUE_D).set_style(stroke_width=1)
        annulus_fill = Circle(radius=2.048 * rate, stroke_width=153.6 * rate, stroke_opacity=0.5, color=BLUE_D)
        origin = Dot(point=ORIGIN, radius=0.07, color="#70AD47")
        player = Dot(point=np.array((0.3, 0.4, 0)), radius=0.07, color="#8C3FC5")
        str1 = Dot(point=np.array((2.5, 2, 0)), radius=0.07, color=RED_E)
        str2 = Dot(point=Line(start=ORIGIN, end=str1.get_center()).rotate(
            angle=(2 * PI) / 3, about_point=ORIGIN).get_end(), radius=0.07, color=RED_E)
        str3 = Dot(point=Line(start=ORIGIN, end=str1.get_center()).rotate(
            angle=-(2 * PI) / 3, about_point=ORIGIN).get_end(), radius=0.07, color=RED_E)
        c_str = Dot(point=np.array((2.5, 2, 0)), radius=0.07, color=YELLOW_D)
        ps1l = Line(start=player.get_center(), end=str1.get_center())
        ps2l = DashedLine().add_updater(
            lambda obj: obj.become(
                DashedLine(start=player.get_center(), end=str2.get_center(), dash_length=0.2, stroke_width=2)))
        ps3l = DashedLine().add_updater(
            lambda obj: obj.become(
                DashedLine(start=player.get_center(), end=str3.get_center(), dash_length=0.2, stroke_width=2)))
        os2l = Line(start=ORIGIN, end=str2.get_center(), color=RED)
        os3l = Line(start=ORIGIN, end=str3.get_center(), color=RED)
        ps1c = Circle(
            radius=Line(start=player.get_center(), end=str1.get_center()).get_length(),
            arc_center=player.get_center(), stroke_width=3, color=RED
        ).rotate(angle=Line(start=player.get_center(), end=str1.get_center()).get_angle())
        run_dot = Dot(point=np.array((2.5, 2, 0))).set_opacity(0)
        ps1c_trace = TracedPath(run_dot.get_center, stroke_width=3).set_color(RED)
        self.camera.frame.scale(0.5)
        self.add(gird, arc_2816, arc_1280, annulus_fill, origin, ps1c_trace, str1, player, keys_and_texts_1)
        str1.add_updater(lambda obj: self.bring_to_front(obj))
        origin.add_updater(lambda obj: self.bring_to_front(obj))
        player.add_updater(lambda obj: self.bring_to_front(obj))
        self.play(
            self.camera.frame.animate.scale(2),
            LaggedStart(
                ShowCreation(ps1l),
                ShowCreationThenDestruction(ps1l.copy().set_color("#8C3FC5")),
                run_time=3,
                lag_ratio=0.9,
                rate_func=rush_from
            )
        )
        self.wait()
        self.play(
            LaggedStart(
                AnimationGroup(
                    ShowCreationThenDestruction(os2l),
                    ShowCreationThenDestruction(os3l),
                ),
                AnimationGroup(
                    GrowFromCenter(str2),
                    GrowFromCenter(str3),
                ),
                run_time=3,
                lag_ratio=0.3,
                rate_func=rush_from
            )
        )
        self.wait()
        str2.add_updater(lambda obj: self.bring_to_front(obj))
        str3.add_updater(lambda obj: self.bring_to_front(obj))
        s1t = Text("1", font='Source Han Sans HC Light', font_size=20).move_to(str1.get_center()).shift(UP * 0.3)
        s2t = Text("2", font='Source Han Sans HC Light', font_size=20).move_to(str2.get_center()).shift(UP * 0.3)
        s3t = Text("3", font='Source Han Sans HC Light', font_size=20).move_to(str3.get_center()).shift(UP * 0.3)
        self.play(
            LaggedStart(
                *[FadeInFromPoint(item[0], item[1].get_center()) for item in [(s1t, str1), (s2t, str2), (s3t, str3)]],
                run_time=3,
                lag_ratio=0.3,
                rate_func=rush_from
            )
        )
        self.wait()
        self.play(
            LaggedStart(
                *[FadeOutToPoint(item[0], item[1].get_center()) for item in [(s1t, str1), (s2t, str2), (s3t, str3)]],
                ShowCreationThenDestruction(ps1l.copy().reverse_points().set_color(RED)),
                AnimationGroup(
                    ShowCreation(ps2l),
                    ShowCreation(ps3l),
                ),
                run_time=3,
                lag_ratio=0.7,
                rate_func=rush_from,
            )
        )
        self.wait()
        player.clear_updaters()
        self.play(Indicate(player))
        player.add_updater(lambda obj: self.bring_to_front(obj))
        self.play(
            LaggedStart(
                ShowCreationThenDestruction(ps1l.copy().set_color(RED)),
                MoveAlongPath(run_dot, ps1c),
                lag_ratio=0.6,
                run_time=3,
                rate_func=rush_from
            )
        )
        self.wait()
        self.remove(ps1c_trace).add(ps1c)
        str2.clear_updaters()
        str3.clear_updaters()
        self.play(
            LaggedStart(
                AnimationGroup(
                    Indicate(str2),
                    Indicate(str3),
                ),
                AnimationGroup(
                    ShowCreationThenDestruction(ps1c.copy().set_color(YELLOW)),
                ),
                lag_ratio=0.6,
                run_time=3,
                rate_func=rush_from
            )
        )
        self.wait()
        str1.clear_updaters()
        self.play(
            ps1c.animate.set_color(color=YELLOW_D),
            ReplacementTransform(str1, c_str),
            self.camera.frame.animate.scale(0.5).move_to(
                Line(start=player.get_center(), end=str1.get_center()).get_center()).shift(RIGHT * 1 + DOWN * 0.1),
            run_time=3,
            rate_func=smooth
        )
        self.wait()
        closest_probability = Tex(
            r"{\color[RGB]{255,255,255}\mathsf{P(\textbf{最近的要塞是}{\color[RGB]{244,211,69}\textbf{候选要塞}\mathsf{K}})}}",
            font_size=19).next_to(player.get_center(), RIGHT * 0.5 + DOWN * 0.2)
        equal_outer = Tex(
            r"{\color[RGB]{255,255,255}\mathsf{P({\color[RGB]{207,80,68}\textbf{剩余要塞}}\textbf{位于圆}", r"\textbf{外}", r")}}", r"=",
            r"{\color[RGB]{255,255,255}\mathsf{P(\textbf{最近的要塞是}{\color[RGB]{244,211,69}\textbf{候选要塞}\mathsf{K}})}}",
            font_size=50).move_to(ORIGIN).shift(DOWN * 0.8)
        unequal_inner = Tex(
            r"{\color[RGB]{255,255,255}\mathsf{P({\color[RGB]{207,80,68}\textbf{剩余要塞}}\textbf{位于圆}", r"\textbf{内}", r")}}", r"=",
            r"{\color[RGB]{255,255,255}\mathsf{P(\textbf{最近的要塞是}{\color[RGB]{244,211,69}\textbf{候选要塞}\mathsf{K}})}}",
            font_size=50).move_to(ORIGIN).shift(DOWN * 0.8)
        complementary = Tex(
            r"\mathsf{1-}", r"{\color[RGB]{255,255,255}\mathsf{P({\color[RGB]{207,80,68}\textbf{剩余要塞}}\textbf{位于圆}", r"\textbf{内}", r")}}", r"=",
            r"{\color[RGB]{255,255,255}\mathsf{P(\textbf{最近的要塞是}{\color[RGB]{244,211,69}\textbf{候选要塞}\mathsf{K}})}}",
            font_size=50).move_to(ORIGIN).shift(DOWN * 0.8)
        mask = Rectangle(height=9, width=16).set_fill(color=BLACK, opacity=0.65).set_stroke(opacity=0).move_to(ORIGIN)
        self.play(
            LaggedStart(
                ShowCreationThenDestruction(ps1l.copy().reverse_points().set_color(YELLOW_D)),
                FadeInFromPoint(closest_probability, player.get_center()),
                run_time=3,
                lag_ratio=0.5,
                rate_func=rush_from
            )
        )
        self.wait()
        self.remove(keys_and_texts_1).add(keys_and_texts_2)
        c_str.add_updater(lambda obj: self.bring_to_front(obj))
        str2.add_updater(lambda obj: self.bring_to_front(obj))
        str3.add_updater(lambda obj: self.bring_to_front(obj))
        ps1c.add_updater(lambda obj: self.bring_to_front(obj))
        keys_and_texts_2.add_updater(lambda obj: self.bring_to_front(obj))
        self.play(
            FadeIn(mask),
            self.camera.frame.animate.scale(2).move_to(ORIGIN),
            TransformMatchingTex(closest_probability, equal_outer),
            run_time=3,
            rate_func=smooth
        )
        ps1c.clear_updaters()
        equal_outer.add_updater(lambda obj: self.bring_to_front(obj))
        self.wait()
        self.play(
            ShowCreationThenDestructionAround(equal_outer[0:3]),
            rate_func=smooth
        )
        self.wait()
        str2.clear_updaters()
        str3.clear_updaters()
        self.play(
            str2.animate.shift(0.6 * (ps2l.get_center() - str2.get_center())),
            str3.animate.shift(0.7 * (ps3l.get_center() - str3.get_center())),
            FadeOut(equal_outer[1], DOWN),
            FadeOut(equal_outer[3], DOWN),
            FadeIn(unequal_inner[1], DOWN),
            run_time=3,
            rate_func=smooth
        )
        self.wait()
        self.remove(equal_outer).add(unequal_inner).remove(unequal_inner[3])
        self.play(
            ReplacementTransform(unequal_inner[0], complementary[1]),
            ReplacementTransform(unequal_inner[1:3], complementary[2:4]),
            ReplacementTransform(unequal_inner[4], complementary[5]),
            FadeIn(complementary[0], RIGHT),
            FadeIn(complementary[4], DOWN),
            run_time=3,
            rate_func=smooth
        )
        self.wait()
        self.play(
            ShowCreationThenDestructionAround(complementary[1:4])
        )
        self.wait()


class Scene5(Scene):  # 310
    def waiting(self, second=0, frame=0, fps=60):
        self.wait(second + frame / fps)

    def construct(self):
        # 极坐标系构建算法来自 @乐正垂星 的开源
        def unit(angle):
            return np.array([np.cos(angle), np.sin(angle), 0])

        str1 = ImageMobject('assets\\raster_images\\Frame.png', height=1
                            ).move_to(np.array([4.5 * np.cos(30 * DEGREES), 4.5 * np.sin(30 * DEGREES), 0]))
        ratio = 1.5
        circles = VGroup(*[Circle(
            radius=r * ratio, stroke_width=2, color=GREY, n_components=24, stroke_opacity=0.5) for r in range(20)])
        rays = VGroup(*[Line(start=ORIGIN, end=80 * unit(i * TAU / 12),
                             stroke_width=2, color=GREY, stroke_opacity=0.5) for i in range(12)])
        radar = VGroup(circles, rays)
        origin = Dot(point=ORIGIN, radius=0.1, color="#70AD47")
        radius_line = Line(
            start=np.array([4.5 * np.cos(30 * DEGREES), 4.5 * np.sin(30 * DEGREES), 0]), end=ORIGIN, color=GREY_A)
        radius_line_colored = Line(
            start=np.array([4.5 * np.cos(30 * DEGREES), 4.5 * np.sin(30 * DEGREES), 0]), end=ORIGIN, color=GOLD)
        base_line = Line(start=np.array([4.5 * np.cos(30 * DEGREES), 0, 0]), end=ORIGIN, color=GREY_A)
        vertical_line = DashedLine(start=np.array([4.5 * np.cos(30 * DEGREES), 4.5 * np.sin(30 * DEGREES), 0]),
                                   end=np.array([4.5 * np.cos(30 * DEGREES), 0, 0]), dash_length=0.2, color=GREY_A)
        arc = Arc(radius=0.75, angle=30 * DEGREES, color=BLUE).set_fill(color=BLUE, opacity=0.5)
        arc_line = Line(start=ORIGIN, end=np.array([0.75, 0, 0]), color=GOLD)
        base_line_temp = base_line.copy()
        radius_line_colored_temp = radius_line_colored.copy()
        arc_line_temp = arc_line.copy()
        radius_text = Tex(r"\mathsf{r}", font_size=48, color=GOLD
                          ).move_to(radius_line.get_center()).shift(LEFT* 0.2 + UP * 0.2)
        angle_text = Tex(r"\mathsf{\theta}", font_size=42, color=BLUE
                         ).move_to(Arc(radius=1, angle=30 * DEGREES).point_from_proportion(0.5))
        # self.add(str1)
        self.wait()
        self.bring_to_back(radar)
        self.play(
            # str1.animate.scale(0.2).move_to(np.array([4.5 * np.cos(30 * DEGREES), 4.5 * np.sin(30 * DEGREES), 0])),
            GrowFromCenter(radar),
            GrowFromCenter(origin),
            run_time=1.5,
            rate_func=smooth
        )
        self.wait()
        origin.add_updater(lambda obj: self.bring_to_front(obj))
        location_text = Tex(r"\mathsf{(}", r"\mathsf{r}", r"\mathsf{, }", r"\mathsf{\theta}", r"\mathsf{)}",
                            font_size=42, color=WHITE, tex_to_color_map={r"r": GOLD, r"\theta": BLUE}
                            ).move_to(str1.get_center()).shift(RIGHT * 1 + DOWN * 0.1)
        self.add(str1)
        str1.add_updater(lambda obj: self.bring_to_front(obj))
        self.play(
            self.camera.frame.animate.scale(0.7).move_to(str1.get_center()).shift(LEFT * 1.3 + DOWN * 1.2),
            LaggedStart(
                AnimationGroup(
                    LaggedStart(
                        AnimationGroup(
                            ShowCreation(radius_line),
                            ShowCreation(vertical_line),
                        ),
                        ShowCreation(base_line),
                        lag_ratio=0.7,
                        rate_func=smooth,
                    )
                ),
                AnimationGroup(
                    ShowCreation(radius_line_colored),
                    Write(radius_text),
                ),
                ShowCreation(arc_line),
                AnimationGroup(
                    ShowCreation(arc),
                    # 以下代码用于将角度符号置于画面最底图层
                    ShowCreation(base_line_temp, run_time=0.1),
                    ShowCreation(radius_line_colored_temp, run_time=0.1),
                    ShowCreation(arc_line_temp, run_time=0.1),
                    Write(angle_text)
                ),
                Write(location_text),
                run_time=2,
                lag_ratio=1,
                rate_func=smooth
            ),
        )
        self.wait()
        str1.clear_updaters()
        str1.add_updater(lambda obj: self.bring_to_front(obj))
        str2 = ImageMobject(
            'assets\\raster_images\\Frame.png', height=1
        ).move_to(Line(start=ORIGIN, end=str1.get_center()).rotate(angle=(2 * PI) / 3, about_point=ORIGIN).get_end())
        str3 = ImageMobject('assets\\raster_images\\Frame.png', height=1).move_to(Line(
            start=ORIGIN, end=str1.get_center()).rotate(angle=-(2 * PI) / 3, about_point=ORIGIN).get_end())
        str2.shift(0.1 * (str2.get_center() - ORIGIN))
        str3.shift(-0.25 * (str3.get_center() - ORIGIN))
        os2l = Line(start=ORIGIN, end=str2.get_center(), color=GREY_A)
        os3l = Line(start=ORIGIN, end=str3.get_center(), color=GREY_A)
        str1.add_updater(lambda obj: obj.become(
            ImageMobject('assets\\raster_images\\Frame.png', height=1).move_to(radius_line.get_start())))
        str2.add_updater(lambda obj: obj.become(
            ImageMobject('assets\\raster_images\\Frame.png', height=1).move_to(os2l.get_end())))
        str3.add_updater(lambda obj: obj.become(
            ImageMobject('assets\\raster_images\\Frame.png', height=1).move_to(os3l.get_end())))
        arc1 = Arc(radius=1.5, angle=120 * DEGREES, color=GOLD).rotate(angle=-90 * DEGREES, about_point=ORIGIN)
        arc2 = Arc(radius=1.5, angle=120 * DEGREES, color=GOLD).rotate(angle=30 * DEGREES, about_point=ORIGIN)
        arc3 = Arc(radius=1.5, angle=120 * DEGREES, color=GOLD).rotate(angle=150 * DEGREES, about_point=ORIGIN)
        arc1_buff = Arc(radius=2.25, angle=120 * DEGREES).rotate(angle=-90 * DEGREES, about_point=ORIGIN).set_opacity(0)
        arc2_buff = Arc(radius=2.25, angle=120 * DEGREES).rotate(angle=30 * DEGREES, about_point=ORIGIN).set_opacity(0)
        arc3_buff = Arc(radius=2.25, angle=120 * DEGREES).rotate(angle=150 * DEGREES, about_point=ORIGIN).set_opacity(0)
        angle_text_120_1 = Tex(r"\mathsf{120^{\circ}}", color=GOLD).add_updater(
            lambda obj: obj.move_to(arc1_buff.point_from_proportion(0.5)))
        angle_text_120_2 = Tex(r"\mathsf{120^{\circ}}", color=GOLD).add_updater(
            lambda obj: obj.move_to(arc2_buff.point_from_proportion(0.5)))
        angle_text_120_3 = Tex(r"\mathsf{120^{\circ}}", color=GOLD).add_updater(
            lambda obj: obj.move_to(arc3_buff.point_from_proportion(0.5)))
        self.play(
            self.camera.frame.animate.scale(2).move_to(ORIGIN),
            *[FadeOut(item) for item in [radius_line_colored, vertical_line, base_line, arc_line, arc, location_text, angle_text, radius_text, base_line_temp, arc_line_temp, radius_line_colored_temp]],
            *[ShowCreation(item) for item in [os2l, os3l, str2, str3]],
            run_time=2,
            rate_func=smooth,
        )
        self.wait()
        [always_rotate(item, rate=0.1, about_point=ORIGIN) for item in
         [os2l, os3l, radius_line, arc1, arc2, arc3, arc1_buff, arc2_buff, arc3_buff]]
        self.play(
            *[ShowCreation(item) for item in [arc1, arc2, arc3, arc1_buff, arc2_buff, arc3_buff]],
            run_time=2,
            rate_func=smooth
        )
        self.waiting(second=4, frame=20)
        self.play(
            *[Write(item) for item in [angle_text_120_1, angle_text_120_2, angle_text_120_3]],
            run_time=2,
            rate_func=smooth
        )
        self.waiting(second=1)
        [item.clear_updaters() for item in
         [os2l, os3l, radius_line, arc1, arc2, arc3, arc1_buff, arc2_buff, arc3_buff, str1, str2, str3, origin]]
        rate = 0.7
        snap_area_1 = Circle(radius=1.28 * np.sqrt(2) * rate, color=BLUE_B, stroke_width=1.5
                             ).set_fill(color=BLUE, opacity=0.5).move_to(str1.get_center())
        snap_area_2 = Circle(radius=1.28 * np.sqrt(2) * rate, color=BLUE_B, stroke_width=1.5
                             ).set_fill(color=BLUE, opacity=0.5).move_to(str2.get_center())
        snap_area_3 = Circle(radius=1.28 * np.sqrt(2) * rate, color=BLUE_B, stroke_width=1.5
                             ).set_fill(color=BLUE, opacity=0.5).move_to(str3.get_center())
        run_dot = Dot(point=str3.get_center()).set_opacity(0)
        trace = TracedPath(run_dot.get_center, stroke_width=1.3).set_color(color=BLUE)
        temp_line = Line(start=str3.get_center(), end=run_dot.copy().shift(
                RIGHT * 1.28 * np.sqrt(2) * rate).get_center(), stroke_width=1.3, color=BLUE)
        snap_text = Tex(r"\mathsf{R=128\sqrt{2}}", font_size=13).move_to(temp_line.get_center()).shift(UP * 0.1)
        str3.save_state()
        self.camera.frame.save_state()
        self.bring_to_back(trace)
        self.play(
            self.camera.frame.animate.scale(0.2).move_to(str3.get_center()).shift(UP * 0.8),
            *[FadeOut(item) for item in [os2l, os3l, radius_line, arc1, arc2, arc3, str1, str2, radar,
                                         origin, angle_text_120_1, angle_text_120_2, angle_text_120_3]],
            str3.animate.scale(0.45),
            run_time=2,
            rate_func=smooth
        )
        self.play(
            LaggedStart(
                run_dot.animate.shift(RIGHT * 1.28 * np.sqrt(2) * rate),
                Write(snap_text)
            ),
        )
        self.wait()
        self.play(
            MoveAlongPath(run_dot, snap_area_3)
        )
        self.remove(run_dot).bring_to_back(snap_area_3)
        self.play(
            FadeIn(snap_area_3)
        )
        self.wait()
        self.remove(trace).add(temp_line).bring_to_back(radar, temp_line, snap_area_3, os3l, str3)
        self.play(
            FadeOut(temp_line),
            FadeOut(snap_text),
            *[FadeIn(item) for item in [arc1, arc2, arc3, snap_area_1, snap_area_2, os2l, os3l, radius_line, str1,
                                        str2, radar, origin, angle_text_120_1, angle_text_120_2, angle_text_120_3]],
            self.camera.frame.animate.restore().shift(UP * 0.7),
            str3.animate.restore(),
            run_time=2,
            rate_func=smooth
        )
        self.wait()
        origin.add_updater(lambda obj: self.bring_to_front(obj))
        str1_dot = Dot(point=str1.get_center(), radius=0.1, color=RED_E)
        str2_dot = Dot(point=str2.get_center(), radius=0.1, color=RED_E)
        str3_dot = Dot(point=str3.get_center(), radius=0.1, color=RED_E)

        snap_dot_2 = Dot(point=str2.get_center()).shift(
            ((1.5 * rate) / os2l.get_length()) * (ORIGIN - str2.get_center())
        ).rotate(angle=PI / 2, about_point=str2_dot.get_center())
        snap_line_2 = Line(start=ORIGIN, end=snap_dot_2.get_center(), color=GREY_A)
        # 利用向量夹角的余弦值公式计算偏移角度Δ，下同
        snap_angle_2 = np.arccos(
            ((str2.get_center()[0] * snap_dot_2.get_center()[0]) + (str2.get_center()[1] * snap_dot_2.get_center()[1]))
            / (os2l.get_length() * snap_line_2.get_length()))
        snap_arc_2 = Arc(angle=snap_angle_2, radius=1.5, color=BLUE
                         ).rotate(angle=snap_line_2.get_angle(), about_point=ORIGIN).reverse_points()
        snap_arc_2_buff = Arc(angle=snap_angle_2, radius=1.9, color=BLUE
                         ).rotate(angle=snap_line_2.get_angle(), about_point=ORIGIN).reverse_points()
        old_line_2 = DashedLine(start=ORIGIN, end=str2_dot.get_center(), dash_length=0.2, color=GREY)
        old_dot_2 = str2_dot.copy().set_color(GREY)

        snap_dot_3 = Dot(point=str3.get_center()).shift(
            ((1.28 * rate) / os3l.get_length()) * (ORIGIN - str3.get_center())
        ).rotate(angle=-PI / 2, about_point=str3_dot.get_center())
        snap_line_3 = Line(start=ORIGIN, end=snap_dot_3.get_center(), color=GREY_A)
        snap_angle_3 = np.arccos(
            ((str3.get_center()[0] * snap_dot_3.get_center()[0]) + (str3.get_center()[1] * snap_dot_3.get_center()[1]))
            / (os3l.get_length() * snap_line_3.get_length()))
        snap_arc_3 = Arc(angle=-snap_angle_3, radius=1.5, color=BLUE
                         ).rotate(angle=snap_line_3.get_angle(), about_point=ORIGIN).reverse_points()
        snap_arc_3_buff = Arc(angle=-snap_angle_3, radius=1.8, color=BLUE
                         ).rotate(angle=snap_line_3.get_angle(), about_point=ORIGIN).reverse_points()
        old_line_3 = DashedLine(start=ORIGIN, end=str3_dot.get_center(), dash_length=0.2, color=GREY)
        old_dot_3 = str3_dot.copy().set_color(GREY)

        snap_angle_text = Tex(r"\mathsf{120^{\circ}}", r"\mathsf{\pm}", r"{\Delta}",
                              tex_to_color_map={r"{\Delta}": BLUE, r"\mathsf{120^{\circ}}": GOLD}
                              ).move_to(arc3_buff.point_from_proportion(0.5))
        delta_1 = Tex(r"{\Delta}", r"\mathsf{_{1}}", color=BLUE, font_size=30
                      ).move_to(snap_arc_2_buff.point_from_proportion(0.5))
        delta_2 = Tex(r"{\Delta}", r"\mathsf{_{2}}", color=BLUE, font_size=30
                      ).move_to(snap_arc_3_buff.point_from_proportion(0.5))

        self.play(
            self.camera.frame.animate.scale(0.6).move_to(
                Line(start=str2, end=str3).get_center()).shift(LEFT * 0.15 + UP * 0.2),
            *[FadeOutToPoint(item, item.get_center()) for item in [str1, str2, str3, angle_text_120_1, angle_text_120_2]],
            FadeOutToPoint(arc1, ORIGIN),
            FadeOutToPoint(arc2, ORIGIN),
            *[FadeIn(item) for item in [str1_dot, str2_dot, str3_dot]],
            run_time=2,
            rate_func=smooth
        )
        self.add(old_dot_2, old_line_2, snap_arc_2, os2l, old_dot_3, old_line_3, snap_arc_3, os3l
                 ).bring_to_front(os2l, str2_dot, os3l, str3_dot)
        self.play(
            ShowCreation(snap_arc_2),
            os2l.animate.put_start_and_end_on(start=ORIGIN, end=snap_dot_2.get_center()),
            str2_dot.animate.move_to(snap_dot_2.get_center()),
            ShowCreation(snap_arc_3),
            os3l.animate.put_start_and_end_on(start=ORIGIN, end=snap_dot_3.get_center()),
            str3_dot.animate.move_to(snap_dot_3.get_center()),
            TransformMatchingTex(angle_text_120_3, snap_angle_text),
            run_time=2,
            rate_func=smooth
        )
        self.wait()
        self.play(
            ReplacementTransform(snap_angle_text[2].copy(), delta_1[0]),
            ReplacementTransform(snap_angle_text[2].copy(), delta_2[0]),
            Write(delta_1[1]),
            Write(delta_2[1]),
            run_time=1,
            rate_func=smooth
        )
        self.wait()
        self.play(
            LaggedStart(
                LaggedStart(
                    self.camera.frame.animate.move_to(str1_dot.get_center()),
                    FadeOutToPoint(snap_area_1, str1_dot.get_center()),
                    lag_ratio=0.8,
                ),
                Indicate(str1_dot),
                run_time=2,
                lag_ratio=0.5,
                rate_func=smooth
            ),
        )
        self.wait()
        self.play(
            self.camera.frame.animate.restore().scale(0.9),
        )
        self.wait()
        self.play(
            *[Indicate(item) for item in [delta_1, delta_2, snap_angle_text[2]]],
        )
        self.wait()
        str1_dot.add_updater(lambda obj: self.bring_to_front(obj))
        self.play(
            LaggedStart(
                ShowCreationThenDestruction(radius_line.copy().set_color(YELLOW)),
                AnimationGroup(
                    ShowCreationThenDestruction(os2l.copy().set_color(YELLOW)),
                    ShowCreationThenDestruction(os3l.copy().set_color(YELLOW)),
                ),
                AnimationGroup(
                    Indicate(str2_dot),
                    Indicate(str3_dot),
                ),
                run_time=2,
                lag_ratio=0.5,
                rate_func=rush_from
            )
        )
        self.wait()
        self.play(
            ShowCreationThenDestructionAround(snap_angle_text)
        )
        self.wait()
        self.play(
            self.camera.frame.animate.scale(0.5).move_to(snap_angle_text.get_center()),
            run_time=15,
            rate_func=smooth
        )


class Scene6(Scene):  # 20
    def construct(self):
        formula = Tex(r"{\color[RGB]{64,62,59}P_{\text{最终}}", r"=", r"P(", r"\text{测量的误差}", r")\cdot P(", r"\text{最近的要塞}", r")}}", font_size=72)
        self.play(
            GrowFromCenter(formula[0]),
            run_time=1.5,
            rate_func=smooth,
        )
        self.wait()
        self.play(
            LaggedStart(
                GrowFromCenter(formula[1]),
                AnimationGroup(
                    GrowFromCenter(formula[2]),
                    GrowFromCenter(formula[4]),
                    GrowFromCenter(formula[6]),
                )
            )
        )
        self.wait()


class Scene7(Scene):  # 168
    def construct(self):
        def value_updater(value):
            return lambda obj: obj.set_value(value * 0.2 * value_tracker.get_value()).move_to(
                target_dot_group_trans[num_list.index(value)])

        # 这是待会要用到的神奇妙妙速率函数
        def slow_out(t: float):
            return 0.7 * (t - 0.9266) ** 9 + 1.7 * (t - 0.9266) ** 3 + 1

        axes = Axes(
            x_range=(-960, 960),
            y_range=(-540, 540),
            height=9,
            width=16,
            axis_config={"include_tip": True, "include_ticks": False},
        ).move_to(ORIGIN)
        coord_group = [(x, y) for y in range(-540, 540) for x in range(-960, 960) if
                       ((x - 12) / 24) % 1 == 0 and ((y - 12) / 24) % 1 == 0]
        dot_group = VGroup(*[Dot(point=axes.c2p(item[0], item[1]), radius=0.007, color=GREY_C) for item in coord_group])
        vertical_dots = VGroup()
        temp = VGroup()
        for idx in range(0, len(dot_group)):
            if dot_group[idx].get_center()[1] == dot_group[idx - 1].get_center()[1]:
                temp.add(dot_group[idx])
            else:
                temp = VGroup(dot_group[idx])
            vertical_dots.add(temp)
        rate = 1.3
        text_1280 = Text('R=1280', font='Source Han Sans HC Light', font_size=18, color=BLUE_B)
        text_2816 = Text('R=2816', font='Source Han Sans HC Light', font_size=18, color=BLUE_B)
        arc_text_1280 = arc_text(text=text_1280, radius=1.28 * rate, angle=30, arc_buff=5
                                 ).set_color(color=BLUE_D).set_style(stroke_width=1)
        arc_text_2816 = arc_text(text=text_2816, radius=2.816 * rate, angle=20, arc_buff=2
                                 ).set_color(color=BLUE_D).set_style(stroke_width=1)
        annulus_fill = Circle(radius=2.048 * rate, stroke_width=153.6 * rate, stroke_opacity=0.5, color=BLUE_D)
        origin = Dot(point=ORIGIN, radius=0.05, color="#70AD47")
        # 参数定义
        player_x, player_y = 50, -120
        cle_x, cle_y = 1034, 1100
        fov_x = 1000
        sigma = 7.3
        player = Dot(point=axes.c2p(player_x, player_y), radius=0.05, color="#8C3FC5")
        # 构建中心直线
        central_line = Line(start=player.get_center(), end=axes.c2p(cle_x, cle_y), stroke_width=2.5, color="#E73750")
        # 获取中心直线的倾斜角并计算视野上下界的倾斜角
        theta_1 = central_line.get_angle() - (sigma * DEGREES)
        theta_2 = central_line.get_angle() + (sigma * DEGREES)
        # 根据给定的视野上下界x轴坐标计算y轴坐标
        fov1_y = (np.tan(theta_1) * (fov_x - player_x)) + player_y
        fov2_y = (np.tan(theta_2) * (fov_x - player_x)) + player_y
        # 构建视野上下界
        fov1_l = DashedLine(start=player.get_center(), end=axes.c2p(fov_x, fov1_y), stroke_width=1.5, color="#8B8B8B",
                            dash_length=0.2).set_opacity(0.7)
        fov2_l = DashedLine(start=player.get_center(), end=axes.c2p(fov_x, fov2_y), stroke_width=1.5, color="#8B8B8B",
                            dash_length=0.2).set_opacity(0.7)
        # 获取候选要塞坐标集合
        target_list, not_target_list = cords_generator(
            player.get_center()[0], player.get_center()[1], fov1_l.get_slope(), fov2_l.get_slope(),
            1.28 * rate, 2.816 * rate, dot_group)
        # 构建候选要塞点集合
        target_dot_group = VGroup(
            *[Dot(point=np.array((item[0], item[1], 0)), radius=0.02, color=YELLOW_D) for item in target_list])
        not_target_dot_group = VGroup(
            *[Dot(point=np.array((item[0], item[1], 0)), radius=0.007, color=GREY_C) for item in not_target_list])
        print(len(target_dot_group))
        target_dot_group_trans = VGroup(*[Dot(radius=0.05, color=YELLOW_D) for _ in range(len(target_dot_group))])
        target_dot_group_trans.arrange_in_grid(n_rows=5, n_cols=8, v_buff=0.3, h_buff=0.5).move_to([2, 0.8, 0])
        mask = Rectangle(
            height=9, width=16).set_fill(color=BLACK, opacity=0.85).set_stroke(opacity=0).move_to([2, 1.3, 0])
        frame = Rectangle(height=10, width=23.5).set_fill(color=BLUE, opacity=0).set_stroke(
            width=2.5, color=WHITE).scale(0.2).move_to(target_dot_group_trans.get_center())
        value_tracker = ValueTracker(1)
        lambda_param = 3.0
        font_size = 15
        num_list = list({32.5, 21.2, 17.8, 9.9, 7.1}.union(set(
            np.clip(np.random.exponential(1 / lambda_param, 35), 0, 7.1))))
        num_list_sorted = sorted(num_list, reverse=True)
        probabilities = VGroup(*[DecimalNumber(
            num_decimal_places=1, font_size=font_size, text_config={'color': YELLOW_D}
        ).add_updater(value_updater(num_list[idx])) for idx in range(len(num_list))])
        probabilities_increased = VGroup(*[DecimalNumber(
            num_decimal_places=1, font_size=font_size
        ).set_value(num_list[idx]).move_to(target_dot_group_trans[idx]) for idx in range(len(num_list))])
        probabilities_arranged = VGroup(*[DecimalNumber(
            num_decimal_places=1, font_size=font_size).set_value(value) for value in num_list_sorted]).arrange(
            DOWN, buff=0.13).move_to([2, 1.3, 0]).align_to([2, 1.3, 0], DOWN).shift(DOWN * 1.8)
        locations = {item.get_value(): item.get_center() for item in probabilities_arranged}
        percentage = Tex(r"\mathsf{\%}", font_size=128).set_opacity(0.2). move_to(target_dot_group_trans.get_center())
        # 配置着色器
        value_to_color = {
            32.5: "#fff600",
            21.2: "#ff6100",
            17.8: "#ff5c00",
            9.9: "#ff2500",
            7.1: "#ff1000"
        }
        for idx in range(len(probabilities)):
            color_matrix = value_to_color.get(probabilities_increased[idx].get_value())
            color_arranged = value_to_color.get(probabilities_arranged[idx].get_value())
            probabilities_increased[idx].set_color(color_matrix)
            probabilities_arranged[idx].set_color(color_arranged)
        # 创建转换动画组
        animation_axe = Axes(
            x_range=(0, 7),
            y_range=(-4, 0),
            height=Line(target_dot_group_trans[0], target_dot_group_trans[32]).get_length(),
            width=Line(target_dot_group_trans[0], target_dot_group_trans[7]).get_length(),
        ).move_to(target_dot_group_trans.get_center())
        anim_dots = VGroup()
        anim_texts = VGroup()
        for r in range(0, 10):
            anim_list_dots_sub = VGroup()
            anim_list_texts_sub = VGroup()
            for idx in range(len(target_dot_group_trans)):
                loc_cor = animation_axe.p2c(target_dot_group_trans[idx].get_center())
                x, y = round(loc_cor[0]), round(loc_cor[1])
                if (r - 1) <= np.sqrt((x ** 2) + (y ** 2)) <= (r + 1):
                    anim_list_dots_sub.add(target_dot_group_trans[idx])
                    anim_list_texts_sub.add(probabilities[idx])
            anim_dots.add(anim_list_dots_sub)
            anim_texts.add(anim_list_texts_sub)
        background = [not_target_dot_group, arc_text_1280, arc_text_2816, axes, annulus_fill, text_1280, text_2816,
                      central_line, origin, fov1_l, fov2_l, player, percentage, frame]
        self.add(not_target_dot_group, arc_text_1280, arc_text_2816, axes, annulus_fill, text_1280, text_2816,
                 central_line, origin, fov1_l, fov2_l, player, mask, frame, anim_dots)
        self.camera.frame.scale(0.5).move_to([2, 1.3, 0])
        self.wait()
        self.play(
            LaggedStart(
                *[ReplacementTransform(anim_dots[idx], anim_texts[idx]) for idx in range(len(anim_dots))],
                FadeIn(percentage),
                run_time=3,
                lag_ratio=0.3,
                rate_func=rush_from
            ),
        )
        self.wait()
        self.play(
            value_tracker.animate.set_value(5),
            run_time=5,
            rate_func=rush_from
        )
        self.play(
            ReplacementTransform(probabilities, probabilities_increased),
            run_time=2,
            rate_func=smooth
        )
        self.wait()
        self.play(
            *[FadeOut(item) for item in background],
            *[item.animate.move_to(locations[item.get_value()]).set_color(WHITE) for item in probabilities_increased],
            run_time=3,
            rate_func=smooth
        )
        self.wait()
        self.remove(probabilities_increased).add(probabilities_arranged)
        probabilities_arranged.add_updater(lambda obj: self.bring_to_front(obj))
        self.play(
            LaggedStart(
                FadeOut(mask),
                self.camera.frame.animate.shift(UP * 7.8),
                run_time=3,
                lag_ratio=0.5,
                rate_func=slow_out
            )
        )
        self.wait()
