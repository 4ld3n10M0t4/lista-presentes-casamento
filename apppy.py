import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lista_casamento.db'
app.config['SECRET_KEY'] = 'chave-casamento-maraisa-aldenio'
db = SQLAlchemy(app)

# Tabelas do Banco de Dados
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    imagem_url = db.Column(db.String(500)) 
    produto_url = db.Column(db.String(500))
    preco = db.Column(db.Float, default=0.0)
    cotas_totais = db.Column(db.Integer, default=1)
    cotas_restantes = db.Column(db.Integer, default=1)
    presenteado = db.Column(db.Boolean, default=False)
    colaboradores = db.relationship('Presenteador', backref='item', lazy=True)

class Presenteador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_convidado = db.Column(db.String(100), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

def setup_db():
    with app.app_context():
        db.create_all()
        if not Item.query.first():
            produtos_raw = [
                {"n": "Geladeira Brastemp 591L", "c": "Eletrodomésticos", "p": 6420.00, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_820475-MLB107416718669_022026-F.jpg", "u": "https://www.mercadolivre.com.br/geladeira-brastemp-bre85mk-591l-frost-free-inverse-inox-xper/up/MLBU3795403303"},
                {"n": "Panela Elétrica De Arroz", "c": "Eletrodomésticos", "p": 360.00, "img": "https://http2.mlstatic.com/D_Q_NP_809829-MLA99927473919_112025-F.jpg", "u": "https://www.mercadolivre.com.br/panela-eletrica-de-arroz-pratic-rice-10i-pe-42-mondial/p/MLB16051362?pdp_filters=item_id%3AMLB2122626365#polycard_client=wishlist&wid=MLB2122626365&sid=bookmarks"},
                {"n": "Air Fryer Forno 12L", "c": "Eletrodomésticos", "p": 519.00, "img": "https://http2.mlstatic.com/D_Q_NP_904318-MLA99523391338_122025-F.jpg", "u": "https://www.mercadolivre.com.br/air-fryer-forno-12l-afon-12l-gi-2000w-digital-mondial-preto-e-inox/p/MLB61696961?pdp_filters=item_id%3AMLB6091369624#polycard_client=wishlist&wid=MLB6091369624&sid=bookmarks"},
                {"n": "Panela Elétrica De Pressão 6L", "c": "Eletrodomésticos", "p": 209.90, "img": "https://http2.mlstatic.com/D_Q_NP_920396-MLA99501531088_112025-F.jpg", "u": "https://www.mercadolivre.com.br/panela-eletrica-de-presso-pe-60-6l-digital-6l-mondial/p/MLB40343565#polycard_client=wishlist&wid=MLB6131070534&sid=bookmarks"},
                {"n": "Micro-ondas 2L", "c": "Eletrodomésticos", "p": 799.00, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_984550-MLA99477052664_112025-F.jpg", "u": "https://www.mercadolivre.com.br/micro-ondas-com-menu-facil-32-litros-cms46ar-cinza-espelhado-consul/p/MLB19310683?pdp_filters=item_id%3AMLB5314935406#polycard_client=wishlist&wid=MLB5314935406&sid=bookmarks"},
                {"n": "Press Grill Master Press Mondial", "c": "Eletrodomésticos", "p": 150.28, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_996722-MLA96151059127_102025-F.jpg", "u": "https://www.mercadolivre.com.br/press-grill-master-press-mondial-1000w-pg-01/p/MLB22338465?pdp_filters=item_id%3AMLB5904304110#polycard_client=wishlist&wid=MLB5904304110&sid=bookmarks"},
                {"n": "Máquina De Lavar Consul 15kg", "c": "Eletrodomésticos", "p": 2099.00, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_868071-MLA99538610488_122025-F.jpg", "u": "https://www.mercadolivre.com.br/consul-lavadoras-cwn15ab-corrente-domestica-220v-branco/p/MLB39328201"},
                {"n": "Fogão 5 Bocas Consul Inox", "c": "Eletrodomésticos", "p": 1611.00, "img": "https://http2.mlstatic.com/D_Q_NP_622742-MLA99943269457_112025-F.jpg", "u": "https://www.mercadolivre.com.br/fogo-de-piso-5-bocas-consul-cfs5nar-acendimento-automatico-cor-inox/p/MLB15295566"},
                {"n": "Forno Elétrico Philco 65L", "c": "Eletrodomésticos", "p": 930.90, "img": "https://http2.mlstatic.com/D_Q_NP_905538-MLA100275580524_122025-F.jpg", "u": "https://www.mercadolivre.com.br/forno-eletrico-philco-65l-dupla-resistncia-pfe65/p/MLB47001375"},
                {"n": "Cafeteira Espresso", "c": "Eletrodomésticos", "p": 599.90, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_608109-MLA100080592963_122025-F.jpg", "u": "https://www.mercadolivre.com.br/cafeteira-espresso-dolce-crema-20-bar-mondial-c-20-ec/p/MLB37878856"},
                {"n": "Chaleira Elétrica Pratic Mondial", "c": "Cozinha", "p": 199.00, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_975907-MLA87312090234_072025-F.jpg", "u": "https://www.mercadolivre.com.br/chaleira-eletrica-pratic-mondial-1200w-ce-06/p/MLB8980300?pdp_filters=item_id%3AMLB4447631701#polycard_client=wishlist&wid=MLB4447631701&sid=bookmarks"},
                {"n": "Jogo Panelas Tramontina", "c": "Cozinha", "p": 695.00, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_731238-MLA88058823610_072025-F.jpg", "u": "https://www.mercadolivre.com.br/jogo-de-panelas-tramontina-aluminio-milazzo-amndoas-7-pc/p/MLB44291059"},
                {"n": "Aparelho De Jantar 30 Peças", "c": "Cozinha", "p": 596.59, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_643687-MLA96120281973_102025-F.jpg", "u": "https://www.mercadolivre.com.br/aparelho-de-jantar-e-cha-30-pecas-oxford-unni-brisa/p/MLB32811621"},
                {"n": "Jogo 3 Travessa Assadeira", "c": "Cozinha", "p": 383.85, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_913983-MLB47575172884_092021-F.jpg", "u": "https://www.mercadolivre.com.br/jogo-3-travessa-assadeira-bake-oxford-grande-branca-25l/up/MLBU1297707018?pdp_filters=item_id%3AMLB2028099681#polycard_client=wishlist&wid=MLB2028099681&sid=bookmarks"},
                {"n": "Porta Tempero Giratório Aço Inox 16 Potes", "c": "Cozinha", "p": 139.90, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_855595-MLB102445077885_122025-F.jpg", "u": "https://www.mercadolivre.com.br/porta-tempero-condimentos-giratorio-aco-inox-16-potes-vidro/up/MLBU3691806089?pdp_filters=item_id%3AMLB6096668902#polycard_client=wishlist&wid=MLB6096668902&sid=bookmarks"},
                {"n": "Panela Pipoqueira Tramontina 3,5l", "c": "Cozinha", "p": 199.99, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_918727-MLA95940134625_102025-F.jpg", "u": "https://www.mercadolivre.com.br/panela-pipoqueira-tramontina-35l-faz-pipoca-docesalgada-cor-preto/p/MLB24769863?pdp_filters=item_id%3AMLB3962892485#polycard_client=wishlist&wid=MLB3962892485&sid=bookmarks"},
                {"n": "Cuscuzeira Antiaderente", "c": "Cozinha", "p": 199.00, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_603927-MLB95126120539_102025-F.jpg", "u": "https://www.mercadolivre.com.br/cuscuzeira-antiaderente-cozivapore-legumes-tramontina-16cm/up/MLBU1471032696?pdp_filters=item_id%3AMLB4382044622#polycard_client=wishlist&wid=MLB4382044622&sid=bookmarks"},
                {"n": "Conjunto Com Jarra E 6 Copos", "c": "Cozinha", "p": 137.99, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_677008-MLB81986821082_022025-F.jpg", "u": "https://www.mercadolivre.com.br/conjunto-com-jarra-e-6-copos-em-vidro-lila--borda-dourada/up/MLBU2996709579?pdp_filters=item_id%3AMLB3967738221#polycard_client=wishlist&wid=MLB3967738221&sid=bookmarks"},
                {"n": "Jogo Completo Utensílios De Cozinha 19", "c": "Cozinha", "p": 135.90, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_709596-MLB98159968024_112025-F.jpg", "u": "https://www.mercadolivre.com.br/jogo-completo-utensilios-de-cozinha-19-pecas-preto/up/MLBU3563616465?pdp_filters=item_id%3AMLB4310754273#polycard_client=wishlist&wid=MLB4310754273&sid=bookmarks"},
                {"n": "Kit 6 Copos Vidro 420ml", "c": "Cozinha", "p": 75.99, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_741357-MLA81508960071_122024-F.jpg", "u": "https://www.mercadolivre.com.br/kit-6-copos-vidro-420ml-borda-dourada-versalhes-agua/p/MLB44953853?pdp_filters=item_id%3AMLB4361303883#polycard_client=wishlist&wid=MLB4361303883&sid=bookmarks"},
                {"n": "Jogo De Facas 6 Peças em Aço Inox", "c": "Cozinha", "p": 172.99, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_836718-MLU74410260758_022024-F.jpg", "u": "https://www.mercadolivre.com.br/jogo-de-facas-plenus-6-pecas-em-aco-inox-com-suporte-de-madeira-tramontina/p/MLB27397330?pdp_filters=item_id%3AMLB3564992001#polycard_client=wishlist&wid=MLB3564992001&sid=bookmarks"},
                {"n": "Kit 4 Assadeiras Tramontina Antiaderente", "c": "Cozinha", "p": 289.90, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_985996-MLB93867682068_102025-F.jpg", "u": "https://www.mercadolivre.com.br/kit-4-assadeiras-tramontina-antiaderente-brasil-rasa-e-funda/up/MLBU1739162354?pdp_filters=item_id%3AMLB3662742383#polycard_client=wishlist&wid=MLB3662742383&sid=bookmarks"},
                {"n": "Jogo Frigideira Tramontina", "c": "Cozinha", "p": 210.65, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_905963-MLA96153030161_102025-F.jpg", "u": "https://www.mercadolivre.com.br/jogo-frigideira-tramontina-3-pecas-caribe-aluminio-com-tampa-cor-preto/p/MLB43773133?pdp_filters=item_id%3AMLB4008126681#polycard_client=wishlist&wid=MLB4008126681&sid=bookmarks"},
                {"n": "Conjunto de 6 Taças de Vidro Cristal 460ml", "c": "Cozinha", "p": 78.99, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_926686-MLA105918497015_012026-F.jpg", "u": "https://www.mercadolivre.com.br/conjunto-de-6-tacas-de-vidro-cristal-460ml-para-vinho-agua-luxo-moderna-pasabahce/p/MLB24209612?pdp_filters=item_id%3AMLB3843332375#polycard_client=wishlist&wid=MLB3843332375&sid=bookmarks"},
                {"n": "Faqueiro Tramontina Búzios 72 Peças Aço Inox", "c": "Cozinha", "p": 215.36, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_947483-MLA92890645577_092025-F.jpg", "u": "https://www.mercadolivre.com.br/faqueiro-tramontina-buzios-72-pecas-aco-inox-para-churrasco/p/MLB42101545?pdp_filters=item_id%3AMLB5148441554#polycard_client=wishlist&wid=MLB5148441554&sid=bookmarks"},
                {"n": "Jogo De Jantar E Chá 20 Peças", "c": "Cozinha", "p": 407.67, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_771183-MLA95712551934_102025-F.jpg", "u": "https://www.mercadolivre.com.br/jogo-de-jantar-e-cha-20-pecas-unni-brisa-oxford-aw20-5903/p/MLB33795714?pdp_filters=item_id%3AMLB4481788370#polycard_client=wishlist&wid=MLB4481788370&sid=bookmarks"},
                {"n": "Panela De Pressão Vancouver", "c": "Cozinha", "p": 209.59, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_821832-MLA99571452148_122025-F.jpg", "u": "https://www.mercadolivre.com.br/panela-de-presso-vancouver-20582620-em-aluminio-com-revestimento-interno-e-externo-antiaderente-grafite-tramontina/p/MLB10892513#polycard_client=wishlist&wid=MLB6100215984&sid=bookmarks"},
                {"n": "Poltrona Decorativa Opalas", "c": "Móveis", "p": 642.81, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_803042-MLA95836475129_102025-F.jpg", "u": "https://www.mercadolivre.com.br/luxo-suede-opala-lazer-leitura-premium-escritorio-suede-macias-poltrona-preto-espuma-d23-1-1-1-madeira-marrom/p/MLB24722863?product_trigger_id=MLB24598329&pdp_filters=item_id%3AMLB4779775766&applied_product_filters=MLB24598394&picker=true&quantity=1"},
                {"n": "Sofá Retrátil", "c": "Móveis", "p": 2661.00, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_957019-MLA95115097910_102025-F.jpg", "u": "https://www.mercadolivre.com.br/king-house-br-king-house-premium-verona-molas-bonnel-sofa-preto-suede-velut-2-3-2-plastico-preto-inclui-e-reclinavel/p/MLB27389983"},
                {"n": "Conjunto De Mesa", "c": "Móveis", "p": 950.00, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_838045-MLB95634110042_102025-F-conjunto-de-mesa-com-6-cadeiras-design-ideal-sofisticado.jpg", "u": "https://produto.mercadolivre.com.br/MLB-5822403288-conjunto-de-mesa-com-6-cadeiras-design-ideal-sofisticado-_JM?searchVariation=186347598576#polycard_client=search-desktop&searchVariation=186347598576&search_layout=grid&position=9&type=item&tracking_id=82557768-c755-41e1-ba37-658f3f306b02"},
                {"n": "Poltrona Decorativa Opalas", "c": "Móveis", "p": 642.81, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_803042-MLA95836475129_102025-F.jpg", "u": "https://www.mercadolivre.com.br/luxo-suede-opala-lazer-leitura-premium-escritorio-suede-macias-poltrona-preto-espuma-d23-1-1-1-madeira-marrom/p/MLB24722863?product_trigger_id=MLB24598329&pdp_filters=item_id%3AMLB4779775766&applied_product_filters=MLB24598394&picker=true&quantity=1"},
                {"n": "Rack Para Sala", "c": "Móveis", "p": 666.00, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_772011-MLA93365752456_092025-F.jpg", "u": "https://www.mercadolivre.com.br/movelove-sevilla-jequitibaoff-white-perolizado/p/MLB42439432"},
                {"n": "Ferro a Vapor Ceramic Express", "c": "Eletrodomésticos Pequenos", "p": 202.90, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_710825-MLA99970193679_112025-F.jpg", "u": "https://www.mercadolivre.com.br/ferro-a-vapor-ceramic-express-mondial-1200w-f-40/p/MLB34701621?pdp_filters=item_id%3AMLB4595336160#polycard_client=wishlist&wid=MLB4595336160&sid=bookmarks"},
                {"n": "Ventilador de Coluna 40cm Turbo Mondial", "c": "Eletrodomésticos Pequenos", "p": 319.90, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_924004-MLA99995731933_112025-F.jpg", "u": "https://www.mercadolivre.com.br/ventilador-de-coluna-40cm-turbo-mondial-140w-nvt-40c-8p-b/p/MLB38089078?pdp_filters=item_id%3AMLB3845367613#polycard_client=wishlist&wid=MLB3845367613&sid=bookmarks"},
                {"n": "Pillow Top Protetor De Colchão Queen", "c": "Roupa de Cama", "p": 249.99, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_990572-MLA98667292202_112025-F.jpg", "u": "https://www.mercadolivre.com.br/pillow-top-protetor-de-colcho-400-fios-soft-premium-queen-cor-branco-desenho-do-tecido-liso/p/MLB51450913?pdp_filters=item_id%3AMLB5447623924#polycard_client=wishlist&wid=MLB5447623924&sid=bookmarks"},
                {"n": "Conjunto Kit Travesseiro", "c": "Roupa de Cama", "p": 232.99, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_781493-MLB87434048359_072025-F.jpg", "u": "https://www.mercadolivre.com.br/conjunto-kit-travesseiro-extra-firme--firme-altenburg/up/MLBU1978926251?pdp_filters=item_id%3AMLB3774882629#polycard_client=wishlist&wid=MLB3774882629&sid=bookmarks"},
                {"n": "Kit Edredom Queen", "c": "Roupa de Cama", "p": 192.40, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_745545-MLA99963133053_112025-F.jpg", "u": "https://www.mercadolivre.com.br/kit-edredom-queen-07-pecas-toque-de-linho-com-tecido-400-fios-cor-cinza-desenho-do-tecido-conjunto/p/MLB45935677?pdp_filters=item_id%3AMLB5279697038#polycard_client=wishlist&wid=MLB5279697038&sid=bookmarks"},
                {"n": "Edredom Casal Queen Size", "c": "Roupa de Cama", "p": 299.99, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_759752-MLA99958094345_112025-F.jpg", "u": "https://www.mercadolivre.com.br/ebenezer-shop-coberdrom-casal-premium-coberta-pelo-de-carneiro-preto-liso-queen-22-cm-24-cm/p/MLB52362520?product_trigger_id=MLB52919655&pdp_filters=item_id%3AMLB5491123600&applied_product_filters=MLB52202214&picker=true&quantity=1"},
                {"n": "Jogo De Toalhas Buddemeyer", "c": "Roupa de Cama", "p": 199.90, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_992849-MLA100187157773_122025-F.jpg", "u": "https://www.mercadolivre.com.br/jogo-de-toalhas-buddemeyer-bella-extra-soft-banho-4-grafitecinza-lisa/p/MLB48810551?pdp_filters=item_id%3AMLB4037655191#polycard_client=wishlist&wid=MLB4037655191&sid=bookmarks"},
                {"n": "Jogo De Toalhas Buddemeyer", "c": "Roupa de Cama", "p": 199.90, "img": "https://http2.mlstatic.com/D_NQ_NP_2X_992849-MLA100187157773_122025-F.jpg", "u": "https://www.mercadolivre.com.br/jogo-de-toalhas-buddemeyer-bella-extra-soft-banho-4-grafitecinza-lisa/p/MLB48810551?pdp_filters=item_id%3AMLB4037655191#polycard_client=wishlist&wid=MLB4037655191&sid=bookmarks"}
            ]

            for data in produtos_raw:
                # Regra de Cotas Automática
                p_val = data["p"]
                if p_val >= 6000: ct = 17
                elif p_val >= 2000: ct = 6
                elif p_val >= 1500: ct = 4
                elif p_val >= 900: ct = 3
                elif p_val >= 500: ct = 2
                else: ct = 1

                item = Item(
                    nome=data["n"], categoria=data["c"], preco=p_val,
                    imagem_url=data["img"], produto_url=data["u"],
                    cotas_totais=ct, cotas_restantes=ct
                )
                db.session.add(item)
            db.session.commit()

@app.route("/")
def index():
    itens = Item.query.all()
    categorias = {}
    for item in itens:
        if item.categoria not in categorias:
            categorias[item.categoria] = []
        categorias[item.categoria].append(item)
    return render_template("index.html", categorias=categorias)

@app.route("/presentear/<int:item_id>", methods=["POST"])
def marcar_presente(item_id):
    item = Item.query.get_or_404(item_id)
    nome_convidado = request.form.get("nome_convidado")

    if not nome_convidado:
        flash("Por favor, digite seu nome!", "danger")
        return redirect(url_for("index"))

    if item.cotas_restantes > 0:
        item.cotas_restantes -= 1
        novo_padrinho = Presenteador(nome_convidado=nome_convidado, item_id=item.id)
        db.session.add(novo_padrinho)
        if item.cotas_restantes == 0:
            item.presenteado = True
        db.session.commit()
        flash(f"Obrigado {nome_convidado}! Presente confirmado.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    setup_db()  # Isso garante a criação da tabela 'item' antes do app rodar
    app.run(debug=True)