import pygame
import math

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in Rolling Hexagon")
clock = pygame.time.Clock()

# 六边形参数
s = 50  # 边长
center = [100, height//2]  # 初始中心位置
angle = 0  # 旋转角度（度）
vx = 2  # 水平移动速度
angular_speed = (vx / s) * 60  # 旋转速度（度/帧）

# 小球参数（局部坐标系）
ball_radius = 10
ball_color = (255, 0, 0)
local_x, local_y = 0, 0  # 初始位于六边形中心
local_vx, local_vy = 3, 4  # 局部速度

# 预计算六边形的局部顶点和边信息
local_vertices = [(
    s * math.cos(math.radians(60 * i)),
    s * math.sin(math.radians(60 * i))
) for i in range(6)]

local_edges = []
for i in range(6):
    A = local_vertices[i]
    B = local_vertices[(i+1)%6]
    dx, dy = B[0]-A[0], B[1]-A[1]
    nx, ny = dy, -dx  # 法线向量（顺时针旋转90度）
    length = math.hypot(nx, ny)
    if length != 0:
        nx /= length
        ny /= length
    local_edges.append((A, B, nx, ny))

def distance_point_line_segment(p, a, b):
    ap_x, ap_y = p[0]-a[0], p[1]-a[1]
    ab_x, ab_y = b[0]-a[0], b[1]-a[1]
    dot = ap_x*ab_x + ap_y*ab_y
    ab_len_sq = ab_x**2 + ab_y**2
    if ab_len_sq == 0:
        return math.hypot(ap_x, ap_y)
    t = max(0, min(1, dot/ab_len_sq))
    nearest_x = a[0] + t*ab_x
    nearest_y = a[1] + t*ab_y
    return math.hypot(p[0]-nearest_x, p[1]-nearest_y)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新六边形位置
    center[0] = (center[0] + vx) % (width + s*2)  # 循环移动
    angle = (angle + angular_speed) % 360

    # 更新小球局部位置
    local_x += local_vx
    local_y += local_vy

    # 碰撞检测（局部坐标系）
    for A, B, nx, ny in local_edges:
        p = (local_x, local_y)
        distance = distance_point_line_segment(p, A, B)
        ap_x, ap_y = local_x-A[0], local_y-A[1]
        if (ap_x*nx + ap_y*ny > 0) and (distance <= ball_radius):
            # 速度反射
            dot = local_vx*nx + local_vy*ny
            local_vx -= 2*dot*nx
            local_vy -= 2*dot*ny
            # 位置修正
            overlap = ball_radius - distance
            local_x += nx*overlap
            local_y += ny*overlap
            break

    # 坐标转换
    angle_rad = math.radians(angle)
    rot_x = local_x*math.cos(angle_rad) - local_y*math.sin(angle_rad)
    rot_y = local_x*math.sin(angle_rad) + local_y*math.cos(angle_rad)
    ball_pos = (int(center[0]+rot_x), int(center[1]+rot_y))

    # 绘制
    screen.fill((255, 255, 255))
    # 绘制六边形
    hex_vertices = [(
        center[0] + x*math.cos(angle_rad) - y*math.sin(angle_rad),
        center[1] + x*math.sin(angle_rad) + y*math.cos(angle_rad)
    ) for (x, y) in local_vertices]
    pygame.draw.polygon(screen, (0, 0, 255), hex_vertices, 2)
    # 绘制小球
    pygame.draw.circle(screen, ball_color, ball_pos, ball_radius)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()