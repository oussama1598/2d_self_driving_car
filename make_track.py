import pygame
import json

WIDTH, HEIGHT = 1200, 800
FPS = 60

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

running = True

outer = True

with open('path.json', 'r') as file:
    previous_data = json.loads(file.read())

outer_vertices = previous_data['outer_vertices']
inner_vertices = previous_data['inner_vertices']
starting_point = previous_data['starting_point']
check_points = previous_data['check_points']

points_queue = []

show_lines = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # if len(starting_point) == 0:
            #     starting_point = list(pygame.mouse.get_pos())
            # elif outer:
            #     outer_vertices.append(pygame.mouse.get_pos())
            # else:
            #     inner_vertices.append(pygame.mouse.get_pos())

            if len(points_queue) == 0:
                points_queue.append(pygame.mouse.get_pos())
            else:
                check_points.append([
                    points_queue.pop(),
                    pygame.mouse.get_pos()
                ])

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_lines = not show_lines

            # if event.key == pygame.K_BACKSPACE:
            #     if outer:
            #         outer_vertices.pop()
            #     else:
            #         inner_vertices.pop()

            # if event.key == pygame.K_c:
            #     if outer:
            #         outer_vertices = []
            #     else:
            #         inner_vertices = []

            # if event.key == pygame.K_n:
            #     outer = False

            if event.key == pygame.K_s:
                path_data = json.dumps({
                    'outer_vertices': outer_vertices,
                    'inner_vertices': inner_vertices,
                    'starting_point': starting_point,
                    'check_points': check_points
                })

                with open('path.json', 'w') as file:
                    file.write(path_data)

    screen.fill((0, 0, 0))

    pygame.draw.circle(
        screen,
        (255, 255, 255),
        starting_point,
        5
    )

    for vertex in outer_vertices:
        pygame.draw.circle(
            screen,
            (255, 0, 0),
            vertex,
            5
        )

    for vertex in inner_vertices:
        pygame.draw.circle(
            screen,
            (0, 0, 255),
            vertex,
            5
        )

    for point in points_queue:
        pygame.draw.circle(
            screen,
            (0, 255, 0),
            point,
            5
        )

    for segment in check_points:
        pygame.draw.line(
            screen,
            (255, 255, 255),
            segment[0],
            segment[1]
        )

    if show_lines or outer == False:
        for i in range(len(outer_vertices)):
            pygame.draw.line(
                screen,
                (255, 255, 255),
                outer_vertices[i],
                outer_vertices[i +
                               1] if i != len(outer_vertices) - 1 else outer_vertices[0]
            )

    if show_lines:
        for i in range(len(inner_vertices)):
            pygame.draw.line(
                screen,
                (255, 255, 255),
                inner_vertices[i],
                inner_vertices[i +
                               1] if i != len(inner_vertices) - 1 else inner_vertices[0]
            )

    pygame.display.flip()

pygame.quit()
