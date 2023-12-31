import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta = { #練習3：移動量辞書
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0),
}
def check_bound(obj_rct: pg.Rect):
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: # 横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom: # 縦方向判定
        tate = False
    return yoko, tate
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img_game_over = pg.image.load("ex02/fig/0.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_game_over = pg.transform.rotozoom(kk_img_game_over, 0, 2.0)

    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400)
    bd_img = pg.Surface((20, 20))
    bd_img.set_colorkey((0,0,0))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()
    x, y = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    bd_rct.center = (x,y)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    game_over = False
    game_over_time = 3000
    bom_imgs = []
    for r in range(1, 11):
        bom_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bom_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bom_imgs.append(bom_img)
        bom_img.set_colorkey((0, 0, 0))
        bom_img = bom_imgs[min(tmr // 500, 9)]
        key_lis ={(-5, 0): pg.transform.rotozoom(kk_img, 0, 1.0), 
                  (-5, -5): pg.transform.rotozoom(kk_img, -45, 1.0),
                  (0, -5): pg.transform.flip(pg.transform.rotozoom(kk_img, -90, 1.0), True, False),
                  (+5, -5): pg.transform.flip(pg.transform.rotozoom(kk_img, -45, 1.0), True, False),
                  (+5, 0): pg.transform.flip(kk_img, True, False),
                  (+5, +5): pg.transform.flip(pg.transform.rotozoom(kk_img, 45, 1.0), True, False),
                  (0, +5): pg.transform.flip(pg.transform.rotozoom(kk_img, 90, 1.0), True, False),
                  (-5, +5): pg.transform.rotozoom(kk_img, 45, 1.0),}

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if not game_over and kk_rct.colliderect(bd_rct):  # 練習５：ぶつかってたら
            print("ゲームオーバー")
            return
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for k, mv in delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
            for l, m in key_lis.items():
                if sum_mv[0] == l[0] and sum_mv[1] ==l[1]:
                    kk_img = m  

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) 
        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0,0]
        for key, mv in delta.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] 
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv[0], sum_mv[1]) 
        if check_bound(kk_rct) != (True, True):  # 練習４：はみだし判定
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) 
        screen.blit(kk_img, kk_rct)
     
        bd_rct.move_ip(vx + 0.01*tmr, vy + 0.01*tmr)  # 追加機能２：爆弾を加速させる
        yoko, tate = check_bound(bd_rct)
        if not yoko:  # 練習４：横方向にはみ出たら
            vx *= -1
        if not tate:  # 練習４：縦方向にはみ出たら
            vy *= -1
        screen.blit(bd_img, bd_rct)
        if game_over:
            screen.blit(kk_img, kk_rct)
        else:
            screen.blit(kk_img, kk_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()