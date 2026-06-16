import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),  # 上矢印キー
    pg.K_DOWN: (0, +5),  # 下矢印キー
    pg.K_LEFT: (-5, 0),  # 左矢印キー
    pg.K_RIGHT: (+5, 0),  # 右矢印キー
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：判定結果タプル（横方向判定結果、縦方向判定結果）
    True：画面内、False：画面外
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を5秒間表示する関数
    引数：スクリーンSurface
    戻り値：なし
    """
     # 黒い画面を作る
    black = pg.Surface((WIDTH, HEIGHT))  # 黒い矩形を描画する
    black.set_alpha(180)  # 透明度を設定する
    pg.draw.rect(black, (0, 0, 0), (0, 0, WIDTH, HEIGHT))

    # Game Over の文字を作る
    font = pg.font.Font(None, 100)
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # 泣いているこうかとん画像を作る
    kk_img = pg.image.load("fig/8.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 1.5)
    kk_rct = kk_img.get_rect(center=((WIDTH // 2) - 240, (HEIGHT // 2)))
    kk_rct_2 = kk_img.get_rect(center=((WIDTH // 2) + 240, (HEIGHT // 2)))
    
    # 黒い画面に文字とこうかとんを貼る
    black.blit(txt, txt_rct)
    black.blit(kk_img, kk_rct)
    black.blit(kk_img, kk_rct_2)
    screen.blit(black, (0, 0))

    # スクリーンに貼って表示する
    screen.blit(black, (0, 0))
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    大きさの違うばくだん画像と加速用リストを作る関数
    引数：なし
    戻り値：ばくだん画像リスト，加速リスト
    """
    bb_imgs = []
    bb_accs = []

    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)

    bb_accs = [a for a in range(1, 11)]

    return bb_imgs, bb_accs

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    移動方向ごとのこうかとん画像を作る関数
    引数：なし
    戻り値：移動量タプルをキー，こうかとん画像を値とする辞書
    """

    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)  # こうかとん画像を読み込み

    kk_imgs = {
        (0, 0): kk_img,
        (+5, 0): pg.transform.flip(kk_img, True, False),  # 右
        (-5, 0): kk_img,  # 左
        (0, -5): pg.transform.rotozoom(kk_img, -90, 1.0),  # 上
        (0, +5): pg.transform.rotozoom(kk_img, 90, 1.0),  # 下
        (+5, -5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 45, 1.0),  # 右上
        (+5, +5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -45, 1.0),  # 右下
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 1.0),  # 左上
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 1.0),  # 左下
    }

    return kk_imgs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    # こうかとんの初期化
    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾の初期化
    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)
    vx, vy = +5, +5

    bb_imgs, bb_accs = init_bb_imgs() # 大きさの違うばくだん画像リストと加速リストを作る
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  # こうかとんRectと爆弾Rectが重なったら
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 横方向の移動量
                sum_mv[1] += mv[1]  # 縦方向の移動量

        kk_rct.move_ip(sum_mv)


        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 動きをなかったことにする

        kk_img = kk_imgs[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)


        # 時間に応じてばくだんを大きく速くする
        bb_img = bb_imgs[min(tmr//500, 9)]

        # 画像サイズが変わるのでRectサイズも更新する
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height

        avx = vx * bb_accs[min(tmr//500, 9)]
        avy = vy * bb_accs[min(tmr//500, 9)]

        # 爆弾を動かす
        bb_rct.move_ip(avx, avy)

        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
