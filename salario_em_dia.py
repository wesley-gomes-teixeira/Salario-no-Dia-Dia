import pygame
import sys
import random
import math

# ─────────────────────────────────────────────
#  INICIALIZAÇÃO
# ─────────────────────────────────────────────
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Salário em Dia")
clock = pygame.time.Clock()
FPS = 60

# ─────────────────────────────────────────────
#  CORES
# ─────────────────────────────────────────────
C_BG          = (18, 22, 36)
C_PANEL       = (28, 34, 52)
C_PANEL2      = (36, 44, 66)
C_WHITE       = (240, 245, 255)
C_GRAY        = (140, 150, 170)
C_GREEN       = (72, 199, 142)
C_YELLOW      = (255, 200, 60)
C_RED         = (255, 90, 90)
C_BLUE        = (80, 160, 255)
C_PURPLE      = (160, 100, 255)
C_ORANGE      = (255, 150, 60)
C_DARK_GREEN  = (30, 80, 55)
C_DARK_RED    = (80, 25, 25)
C_ACCENT      = (100, 210, 255)

# ─────────────────────────────────────────────
#  FONTES
# ─────────────────────────────────────────────
font_title  = pygame.font.SysFont("consolas", 36, bold=True)
font_big    = pygame.font.SysFont("consolas", 28, bold=True)
font_med    = pygame.font.SysFont("consolas", 20)
font_small  = pygame.font.SysFont("consolas", 15)
font_tiny   = pygame.font.SysFont("consolas", 13)

# ─────────────────────────────────────────────
#  DADOS DO JOGO
# ─────────────────────────────────────────────
SALARIO = 1800.0

SEMANAS = [
    {
        "nome": "Semana 1 — Chegou o salário!",
        "descricao": "Hora de organizar as contas fixas do mês.",
        "eventos": [
            {
                "titulo": "🏠 Aluguel",
                "texto": "Vencimento hoje! Você paga R$ 700 de aluguel.",
                "opcoes": [
                    {"label": "Pagar agora", "custo": 700, "efeito": 0, "msg": "✅ Aluguel pago. Boa responsabilidade!"},
                    {"label": "Deixar pra depois...", "custo": 780, "efeito": -10, "msg": "⚠️ Multa de atraso. Custou mais caro!"},
                ],
            },
            {
                "titulo": "🛒 Mercado",
                "texto": "Geladeira vazia. Você precisa fazer compras.",
                "opcoes": [
                    {"label": "Lista básica (R$200)", "custo": 200, "efeito": 5, "msg": "✅ Compras planejadas. Bem feito!"},
                    {"label": "Comprar tudo que der vontade", "custo": 420, "efeito": -5, "msg": "😬 Gastou quase o dobro sem perceber."},
                ],
            },
            {
                "titulo": "🚌 Transporte",
                "texto": "Você precisa se locomover todo mês.",
                "opcoes": [
                    {"label": "Cartão mensal (R$150)", "custo": 150, "efeito": 5, "msg": "✅ Econômico e prático!"},
                    {"label": "Aplicativo todo dia (~R$300)", "custo": 300, "efeito": -5, "msg": "📱 Conforto tem custo. São R$150 a mais!"},
                ],
            },
        ],
    },
    {
        "nome": "Semana 2 — Tentações chegam",
        "descricao": "O mês tá bom... ou tá?",
        "eventos": [
            {
                "titulo": "🎉 Rolê com amigos",
                "texto": "Amigos chamam pra balada. Entrada + drinks: ~R$150.",
                "opcoes": [
                    {"label": "Ir e gastar com moderação", "custo": 100, "efeito": 8, "msg": "😄 Lazer é importante! Gasto controlado."},
                    {"label": "Ir e aproveitar sem pensar", "custo": 280, "efeito": -8, "msg": "🍻 Divertiu, mas extrapolou o dobro."},
                    {"label": "Não ir (economizar)", "custo": 0, "efeito": -3, "msg": "💸 Economizou, mas missão social zero."},
                ],
            },
            {
                "titulo": "📱 Celular novo",
                "texto": "Promoção imperdível! Celular novo por R$800 no cartão.",
                "opcoes": [
                    {"label": "Comprar (parcelar)", "custo": 800, "efeito": -15, "msg": "😬 Compra por impulso. Vai apertar!"},
                    {"label": "Esperar juntar dinheiro", "custo": 0, "efeito": 10, "msg": "✅ Disciplina financeira! Inteligente."},
                ],
            },
            {
                "titulo": "📄 Boleto esquecido",
                "texto": "Ops! Boleto do plano de saúde vence hoje. R$120.",
                "opcoes": [
                    {"label": "Pagar agora", "custo": 120, "efeito": 5, "msg": "✅ Saúde em dia. Boa organização!"},
                    {"label": "Ignorar por ora", "custo": 0, "efeito": -10, "msg": "⚠️ Plano suspenso. Risco desnecessário."},
                ],
            },
        ],
    },
    {
        "nome": "Semana 3 — Imprevistos",
        "descricao": "A vida não avisa quando algo vai dar errado.",
        "eventos": [
            {
                "titulo": "🏥 Consulta médica urgente",
                "texto": "Você adoeceu. Consulta particular: R$250. Tem reserva?",
                "opcoes": [
                    {"label": "Pagar a consulta", "custo": 250, "efeito": 10, "msg": "✅ Saúde é prioridade! Cuidado acertado."},
                    {"label": "Ignorar e torcer pra melhorar", "custo": 0, "efeito": -20, "msg": "😰 Piorou. Depois foi ao pronto-socorro. Mais caro!"},
                ],
            },
            {
                "titulo": "🔧 Conserto do notebook",
                "texto": "Notebook parou de funcionar. Precisa pra trabalhar. Reparo: R$300.",
                "opcoes": [
                    {"label": "Consertar agora", "custo": 300, "efeito": 5, "msg": "✅ Ferramenta de trabalho protegida."},
                    {"label": "Pedir emprestado", "custo": 0, "efeito": -5, "msg": "🤝 Funcionou, mas gera dependência."},
                ],
            },
            {
                "titulo": "💰 Oportunidade de poupança",
                "texto": "Banco oferece CDB com rendimento de 12% ao ano. Você investe?",
                "opcoes": [
                    {"label": "Investir R$200", "custo": 200, "efeito": 20, "msg": "🌱 Ótimo! Seu dinheiro começa a trabalhar por você."},
                    {"label": "Não agora", "custo": 0, "efeito": 0, "msg": "🤷 Ok. Mas lembre: dinheiro parado perde valor."},
                ],
            },
        ],
    },
    {
        "nome": "Semana 4 — Fechamento do mês",
        "descricao": "Como você vai entrar no próximo mês?",
        "eventos": [
            {
                "titulo": "🎓 Curso online",
                "texto": "Curso de Python por R$180. Vai agregar na carreira.",
                "opcoes": [
                    {"label": "Investir no curso", "custo": 180, "efeito": 15, "msg": "📚 Investimento em conhecimento sempre vale!"},
                    {"label": "Não agora", "custo": 0, "efeito": 0, "msg": "🤷 Ok. Mas crescimento profissional é ativo."},
                ],
            },
            {
                "titulo": "🍕 Delivery toda noite",
                "texto": "Semana pesada. Você pediu delivery todos os dias: R$350 no total.",
                "opcoes": [
                    {"label": "Aceitar o gasto", "custo": 350, "efeito": -10, "msg": "😬 Conforto caro. Cozinhar economizaria 70%."},
                    {"label": "Já tinha cozinhado em casa", "custo": 80, "efeito": 10, "msg": "✅ Planejamento + cozinha = economia real!"},
                ],
            },
            {
                "titulo": "🏦 Reserva de emergência",
                "texto": "Fim do mês. Você guarda algo pra reserva de emergência?",
                "opcoes": [
                    {"label": "Guardar 10% do salário (R$180)", "custo": 180, "efeito": 25, "msg": "🌟 Perfeito! Reserva = segurança financeira."},
                    {"label": "Gastar o resto", "custo": 0, "efeito": -15, "msg": "😬 Mês que vem, qualquer imprevisto vai doer."},
                ],
            },
        ],
    },
]

# ─────────────────────────────────────────────
#  ESTADO DO JOGO
# ─────────────────────────────────────────────
class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.saldo       = SALARIO
        self.humor       = 50        # 0–100
        self.semana_idx  = 0
        self.evento_idx  = 0
        self.historico   = []        # lista de strings
        self.fase        = "intro"   # intro | jogo | fim
        self.msg_feedback = ""
        self.msg_timer   = 0
        self.animacao_saldo = SALARIO
        self.particulas  = []

    @property
    def semana(self):
        return SEMANAS[self.semana_idx]

    @property
    def evento(self):
        return self.semana["eventos"][self.evento_idx]

    def aplicar_opcao(self, opcao):
        custo  = opcao["custo"]
        efeito = opcao["efeito"]
        self.saldo  = max(0, self.saldo - custo)
        self.humor  = max(0, min(100, self.humor + efeito))
        self.msg_feedback = opcao["msg"]
        self.msg_timer = 180
        entrada = f"S{self.semana_idx+1}E{self.evento_idx+1}: {opcao['label']} → {opcao['msg'][:35]}"
        self.historico.append(entrada)
        # partículas
        for _ in range(18):
            self.particulas.append({
                "x": random.randint(100, WIDTH-100),
                "y": random.randint(100, HEIGHT-100),
                "vx": random.uniform(-2, 2),
                "vy": random.uniform(-3, -0.5),
                "life": random.randint(40, 80),
                "cor": C_GREEN if efeito >= 0 else C_RED,
            })

    def avancar(self):
        self.evento_idx += 1
        if self.evento_idx >= len(self.semana["eventos"]):
            self.evento_idx = 0
            self.semana_idx += 1
            if self.semana_idx >= len(SEMANAS):
                self.fase = "fim"

    def cor_saldo(self):
        pct = self.saldo / SALARIO
        if pct > 0.5: return C_GREEN
        if pct > 0.2: return C_YELLOW
        return C_RED

    def cor_humor(self):
        if self.humor > 60: return C_GREEN
        if self.humor > 30: return C_YELLOW
        return C_RED

    def resultado_final(self):
        if self.saldo > 800 and self.humor > 60:
            return "excelente"
        if self.saldo > 400 and self.humor > 30:
            return "ok"
        return "ruim"

gs = GameState()

# ─────────────────────────────────────────────
#  HELPERS DE DESENHO
# ─────────────────────────────────────────────
def draw_rect_rounded(surf, cor, rect, radius=12, alpha=255):
    s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    pygame.draw.rect(s, (*cor, alpha), (0, 0, rect[2], rect[3]), border_radius=radius)
    surf.blit(s, (rect[0], rect[1]))

def draw_text_wrapped(surf, texto, font, cor, x, y, max_width):
    palavras = texto.split(" ")
    linha = ""
    dy = 0
    for palavra in palavras:
        teste = linha + palavra + " "
        if font.size(teste)[0] > max_width and linha:
            render = font.render(linha.strip(), True, cor)
            surf.blit(render, (x, y + dy))
            dy += font.get_linesize() + 2
            linha = palavra + " "
        else:
            linha = teste
    if linha.strip():
        render = font.render(linha.strip(), True, cor)
        surf.blit(render, (x, y + dy))
    return dy + font.get_linesize()

def draw_bar(surf, x, y, w, h, pct, cor_bg, cor_fill, radius=8):
    draw_rect_rounded(surf, cor_bg, (x, y, w, h), radius)
    fill_w = max(0, int(w * pct))
    if fill_w > 0:
        draw_rect_rounded(surf, cor_fill, (x, y, fill_w, h), radius)

def blit_center(surf, text_surf, cy, cx=WIDTH//2):
    r = text_surf.get_rect(center=(cx, cy))
    surf.blit(text_surf, r)

# ─────────────────────────────────────────────
#  PARTÍCULAS
# ─────────────────────────────────────────────
def update_particulas():
    for p in gs.particulas[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["life"] -= 1
        if p["life"] <= 0:
            gs.particulas.remove(p)

def draw_particulas():
    for p in gs.particulas:
        alpha = int(255 * p["life"] / 80)
        s = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(s, (*p["cor"], alpha), (3, 3), 3)
        screen.blit(s, (int(p["x"]), int(p["y"])))

# ─────────────────────────────────────────────
#  TELA INTRO
# ─────────────────────────────────────────────
btn_start = pygame.Rect(WIDTH//2 - 140, 420, 280, 54)

def draw_intro():
    screen.fill(C_BG)
    # fundo decorativo
    for i in range(8):
        pygame.draw.circle(screen, C_PANEL, (random.randint(0, WIDTH), random.randint(0, HEIGHT)), random.randint(40, 120), 2)

    t = pygame.time.get_ticks() / 1000
    pulse = 1 + 0.04 * math.sin(t * 2)

    # título
    titulo = font_title.render("💰 SALÁRIO EM DIA", True, C_ACCENT)
    blit_center(screen, titulo, 130)

    sub = font_med.render("Um jogo sobre decisões financeiras reais", True, C_GRAY)
    blit_center(screen, sub, 175)

    # card info
    draw_rect_rounded(screen, C_PANEL, (WIDTH//2-260, 210, 520, 180), 16)
    infos = [
        f"💵 Salário mensal: R$ {SALARIO:.0f}",
        "📅 4 semanas de decisões",
        "🎯 Objetivo: chegar no fim no positivo",
        "❤️  Cuide do saldo E do seu bem-estar",
    ]
    for i, info in enumerate(infos):
        t_surf = font_small.render(info, True, C_WHITE)
        screen.blit(t_surf, (WIDTH//2 - 220, 228 + i * 36))

    # botão
    btn_cor = C_ACCENT if btn_start.collidepoint(pygame.mouse.get_pos()) else C_BLUE
    draw_rect_rounded(screen, btn_cor, btn_start, 14)
    btn_txt = font_big.render("▶  COMEÇAR", True, C_BG)
    blit_center(screen, btn_txt, btn_start.centery + 2)

    rodape = font_tiny.render("Tema: Educação Financeira  |  PyGame  |  A3 UDWMJ", True, C_GRAY)
    blit_center(screen, rodape, HEIGHT - 20)

# ─────────────────────────────────────────────
#  HUD TOPO
# ─────────────────────────────────────────────
def draw_hud():
    # painel topo
    draw_rect_rounded(screen, C_PANEL, (10, 10, WIDTH - 20, 70), 12)

    # saldo animado
    gs.animacao_saldo += (gs.saldo - gs.animacao_saldo) * 0.1
    saldo_txt = font_big.render(f"R$ {gs.animacao_saldo:,.2f}", True, gs.cor_saldo())
    screen.blit(saldo_txt, (24, 20))

    label_saldo = font_tiny.render("SALDO", True, C_GRAY)
    screen.blit(label_saldo, (24, 48))

    # semana
    sem_txt = font_small.render(f"Semana {gs.semana_idx+1}/4", True, C_ACCENT)
    screen.blit(sem_txt, (WIDTH//2 - 55, 18))
    ev_txt = font_tiny.render(f"Evento {gs.evento_idx+1}/{len(gs.semana['eventos'])}", True, C_GRAY)
    screen.blit(ev_txt, (WIDTH//2 - 40, 40))

    # barra de humor
    screen.blit(font_tiny.render("BEM-ESTAR", True, C_GRAY), (WIDTH - 180, 14))
    draw_bar(screen, WIDTH-180, 32, 160, 14, gs.humor/100, C_PANEL2, gs.cor_humor(), 7)
    screen.blit(font_tiny.render(f"{gs.humor}%", True, gs.cor_humor()), (WIDTH-180, 50))

# ─────────────────────────────────────────────
#  TELA DE JOGO
# ─────────────────────────────────────────────
opcao_btns = []

def draw_jogo():
    global opcao_btns
    screen.fill(C_BG)
    draw_hud()

    ev = gs.evento
    sem = gs.semana

    # nome da semana
    draw_rect_rounded(screen, C_PANEL, (10, 88, WIDTH-20, 38), 10)
    sem_surf = font_small.render(sem["nome"], True, C_YELLOW)
    screen.blit(sem_surf, (24, 97))

    # card do evento
    card_y = 136
    draw_rect_rounded(screen, C_PANEL, (10, card_y, WIDTH-20, 110), 14)
    titulo_surf = font_med.render(ev["titulo"], True, C_WHITE)
    screen.blit(titulo_surf, (24, card_y + 12))
    draw_text_wrapped(screen, ev["texto"], font_small, C_GRAY, 24, card_y + 42, WIDTH - 60)

    # opções
    n = len(ev["opcoes"])
    btn_h = 68
    gap   = 12
    total = n * btn_h + (n-1) * gap
    start_y = card_y + 130

    opcao_btns = []
    for i, op in enumerate(ev["opcoes"]):
        bx = 10
        by = start_y + i * (btn_h + gap)
        bw = WIDTH - 20
        rect = pygame.Rect(bx, by, bw, btn_h)
        opcao_btns.append(rect)

        hover = rect.collidepoint(pygame.mouse.get_pos())
        bg = C_PANEL2 if not hover else (50, 65, 100)
        draw_rect_rounded(screen, bg, (bx, by, bw, btn_h), 12)

        # borda sutil
        pygame.draw.rect(screen, C_BLUE if hover else C_PANEL, rect, 2, border_radius=12)

        label_surf = font_med.render(op["label"], True, C_WHITE)
        screen.blit(label_surf, (bx + 20, by + 12))

        custo = op["custo"]
        custo_cor = C_RED if custo > 0 else C_GREEN
        custo_txt = f"-R$ {custo:.0f}" if custo > 0 else "Sem custo"
        custo_surf = font_small.render(custo_txt, True, custo_cor)
        screen.blit(custo_surf, (bx + 20, by + 40))

    # feedback
    if gs.msg_timer > 0:
        alpha = min(255, gs.msg_timer * 5)
        s = pygame.Surface((WIDTH-20, 44), pygame.SRCALPHA)
        s.fill((*C_PANEL2, min(200, alpha)))
        screen.blit(s, (10, HEIGHT - 54))
        fb_surf = font_small.render(gs.msg_feedback, True, C_ACCENT)
        screen.blit(fb_surf, (24, HEIGHT - 44))
        gs.msg_timer -= 1

    # partículas
    draw_particulas()

# ─────────────────────────────────────────────
#  TELA FIM
# ─────────────────────────────────────────────
btn_restart = pygame.Rect(WIDTH//2 - 130, HEIGHT - 80, 260, 50)

def draw_fim():
    screen.fill(C_BG)
    resultado = gs.resultado_final()

    emoji_map  = {"excelente": "🏆", "ok": "👍", "ruim": "😰"}
    titulo_map = {"excelente": "MÊS CONCLUÍDO COM SUCESSO!", "ok": "MÊS OK — PODE MELHORAR", "ruim": "MÊS DIFÍCIL..."}
    cor_map    = {"excelente": C_GREEN, "ok": C_YELLOW, "ruim": C_RED}

    draw_rect_rounded(screen, C_PANEL, (20, 20, WIDTH-40, 100), 16)
    t_surf = font_big.render(f"{emoji_map[resultado]} {titulo_map[resultado]}", True, cor_map[resultado])
    blit_center(screen, t_surf, 60)

    # estatísticas
    draw_rect_rounded(screen, C_PANEL, (20, 130, WIDTH-40, 120), 14)
    stats = [
        (f"💰 Saldo final:", f"R$ {gs.saldo:.2f}", gs.cor_saldo()),
        (f"❤️  Bem-estar:", f"{gs.humor}%", gs.cor_humor()),
        (f"📊 Decisões tomadas:", f"{len(gs.historico)}", C_ACCENT),
    ]
    for i, (label, val, cor) in enumerate(stats):
        l_s = font_small.render(label, True, C_GRAY)
        v_s = font_med.render(val, True, cor)
        screen.blit(l_s, (40, 145 + i*34))
        screen.blit(v_s, (360, 145 + i*34))

    # lições
    draw_rect_rounded(screen, C_PANEL, (20, 260, WIDTH-40, 200), 14)
    screen.blit(font_med.render("📚 Lições desta jornada:", True, C_WHITE), (40, 272))
    licoes_map = {
        "excelente": [
            "✅ Você planejou gastos fixos com antecedência.",
            "✅ Manteve equilíbrio entre lazer e economia.",
            "✅ Criou ou reforçou sua reserva de emergência.",
            "💡 Próximo passo: investir regularmente.",
        ],
        "ok": [
            "⚠️ Algumas decisões por impulso pesaram no saldo.",
            "💡 Planeje os gastos antes de receber o salário.",
            "💡 Guarde ao menos 10% todo mês como reserva.",
        ],
        "ruim": [
            "❌ Gastos por impulso comprometeram o orçamento.",
            "❌ Falta de reserva tornou imprevistos críticos.",
            "💡 Regra 50-30-20: necessidades, desejos, reserva.",
            "💡 Todo mês é uma nova chance de melhorar!",
        ],
    }
    for i, licao in enumerate(licoes_map[resultado]):
        l_s = font_small.render(licao, True, C_GRAY)
        screen.blit(l_s, (40, 305 + i * 36))

    # botão reiniciar
    btn_cor = C_ACCENT if btn_restart.collidepoint(pygame.mouse.get_pos()) else C_BLUE
    draw_rect_rounded(screen, btn_cor, btn_restart, 14)
    r_surf = font_med.render("🔄  Jogar Novamente", True, C_BG)
    blit_center(screen, r_surf, btn_restart.centery + 2)

    rodape = font_tiny.render("Tema: Educação Financeira  |  PyGame  |  A3 UDWMJ", True, C_GRAY)
    blit_center(screen, rodape, HEIGHT - 12)

# ─────────────────────────────────────────────
#  GAME LOOP PRINCIPAL
# ─────────────────────────────────────────────
aguardando_avancar = False
btn_avancar = pygame.Rect(WIDTH//2 - 100, HEIGHT - 54, 200, 40)

running = True
while running:
    clock.tick(FPS)

    # ── INPUT ──────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if gs.fase == "intro":
                if btn_start.collidepoint(mx, my):
                    gs.fase = "jogo"

            elif gs.fase == "jogo":
                if not aguardando_avancar:
                    for i, rect in enumerate(opcao_btns):
                        if rect.collidepoint(mx, my):
                            gs.aplicar_opcao(gs.evento["opcoes"][i])
                            aguardando_avancar = True
                            break
                else:
                    # qualquer clique após feedback avança
                    gs.avancar()
                    aguardando_avancar = False

            elif gs.fase == "fim":
                if btn_restart.collidepoint(mx, my):
                    gs.reset()

    # ── UPDATE ─────────────────────────────────
    update_particulas()

    # ── DRAW ───────────────────────────────────
    if gs.fase == "intro":
        draw_intro()
    elif gs.fase == "jogo":
        draw_jogo()
        # botão "continuar" pós-escolha
        if aguardando_avancar:
            draw_rect_rounded(screen, C_ACCENT, btn_avancar, 10)
            c_surf = font_small.render("Clique para continuar →", True, C_BG)
            blit_center(screen, c_surf, btn_avancar.centery + 2)
    elif gs.fase == "fim":
        draw_fim()

    pygame.display.flip()

pygame.quit()
sys.exit()
