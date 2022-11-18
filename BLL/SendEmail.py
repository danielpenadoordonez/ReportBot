from cgitb import html
import smtplib, ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from Clases.Dia import Dia
from Clases.Publicador import Publicador
from BLL import GoalProcess

REPORTBOT_EMAIL = None
REPORTBOT_PASS = None
DEV_EMAIL = None

def load_Creds():
    global REPORTBOT_EMAIL, REPORTBOT_PASS, DEV_EMAIL
    REPORTBOT_EMAIL = os.environ.get("REPORTBOT_EMAIL")
    REPORTBOT_PASS = os.environ.get("REPORTBOT_PASS")
    DEV_EMAIL = os.environ.get("DEV_EMAIL")

def send_New_User_Alert(publicador:Publicador):
    sender = REPORTBOT_EMAIL
    reciever = DEV_EMAIL
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = reciever
    msg['Subject'] = "Nuevo Publicador Registrado"
    body = f"""
    Hay un nuevo usuario del programa
    NOMBRE: {publicador.nombreCompleto}
    """
    msg.attach(MIMEText(body))
    msg = msg.as_string()
    try:
        port = 465
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender, REPORTBOT_PASS)
            server.sendmail(sender, reciever, msg)
    except:
        raise


def envia_Informe_Por_Correo(informe, publicador:Publicador):
    contactos = [publicador.correoPersonal, publicador.correoEncargadoInfs]
    sender = REPORTBOT_EMAIL
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ", ".join(contactos)
    msg['Subject'] = f"Informe de Predicacion {publicador.nombreCompleto.upper()}"
    htmlTable = """
    <html>
    <head>
        <style>
            .publisher-data{
                display: block;
                margin-right: auto;
                margin-left: auto;
                width: 50%;
            }
        </style>
    </head>
    """
    htmlTable += f"""
    <body>
        <br>
        <h1 style="text-align: center;">Informe del Mes</h1>
    <table border="3" style="background-color: lightcyan; width: 65%; text-align: center; margin-left: auto; margin-right: auto;">
        <tr style="height: 50px;">
            <td style="font-weight: bold;">Horas</td>
            <td style="width: 30%;">{informe['Horas']}</td>
        </tr>
        <tr style="height: 50px;">
            <td style="font-weight: bolder;">Publicaciones</td>
            <td style="width: 30%;">{informe['Publicaciones']}</td>
        </tr>
        <tr style="height: 50px;">
            <td style="font-weight: bold;">Videos</td>
            <td style="width: 30%;">{informe['Videos']}</td>
        </tr>
        <tr style="height: 50px;">
            <td style="font-weight: bold;">Revisitas</td>
            <td style="width: 30%;">{informe['Revisitas']}</td>
        </tr>
        <tr style="height: 50px;">
            <td style="font-weight: bold;">Estudios</td>
            <td style="width: 30%;">{informe['Estudios']}</td>
        </tr>
    </table>
    <br>
    <br>
    """
    #Se personaliza si es publicador o publicadora
    if publicador.genero == 'H':
        htmlTable += f"""
        <div class="publisher-data">
        <hr>
        <h4>Publicador: {publicador.nombreCompleto}</h4>
        <h4>Grupo: {publicador.grupo}</h4>
        <hr>
        </div>
        </body>
    </html>
        """
    else:
        htmlTable += f"""
        <div class="publisher-data">
        <hr>
        <h4>Publicadora: {publicador.nombreCompleto}</h4>
        <h4>Grupo: {publicador.grupo}</h4>
        <hr>
        </div>
        </body>
    </html>
        """

    msg.attach(MIMEText(htmlTable, "html"))

    #Se abre el archivo
    #attachmente = open("Informe del Mes.txt",'rb')
    #part = MIMEBase("application", "octet-stream")
    #part.set_payload(attachmente.read())
    #encoders.encode_base64(part)
    #part.add_header("Content-Disposition", f"attachment; filename=Informe del Mes.txt")
    #msg.attach(part)
    msg = msg.as_string()

    try:
        port = 465
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender, REPORTBOT_PASS)
            server.sendmail(sender, contactos, msg)
    except:
        raise

def envia_Reporte_Metas(goalList, informe, publicador:Publicador):
    sender = REPORTBOT_EMAIL
    receiver = publicador.correoPersonal
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Reporte de Metas"
    htmlMessage = """
    <html>
    <head>
        <style>
            #goal-list{
                display: block;
                margin-right: auto;
                margin-left: auto;
            }

            .goal-reached{
                display: block;
                margin-right: auto;
                margin-left: auto;
                width: 70%;
                border-style: solid;
                border-radius: 20px 20px 20px 20px;
                -moz-border-radius: 20px 20px 20px 20px;
                -webkit-border: 20px 20px 20px 20px;
                border-color: lightgreen;
                padding-right: 2%;
                padding-left: 2%;
                background-color: lightgreen;
            }

            .goal-unreached{
                display: block;
                margin-right: auto;
                margin-left: auto;
                width: 70%;
                border-style: solid;
                border-radius: 20px 20px 20px 20px;
                -moz-border-radius: 20px 20px 20px 20px;
                -webkit-border: 20px 20px 20px 20px;
                border-color: crimson;
                padding-right: 2%;
                padding-left: 2%;
                background-color:crimson;
            }
        </style>
    </head>
    <body>
        <br>
        <h1 style="text-align: center; font-weight: bolder; color: darkblue;">MIS METAS</h1>
        <br>
        <div id="goal-list">
    """
    for goal in goalList:
        if GoalProcess.meta_Alcanzada(goal, informe):
            htmlMessage += f"""
            <div class="goal-reached">
                <h2 style="text-align: center;">{goal.nombre}</h2>
                <hr>
                <h4>Tipo de Meta: {goal.tipo.upper()}</h4>
                <h4>Cantidad Meta: {goal.cantidad}</h4>
                <h4>Cantidad Informada: {informe[goal.tipo]}</h4>
                <h2 style="text-align: center;">META ALCANZADA</h2>
            </div>
            <br>
            """
        else:
            htmlMessage += f"""
            <div class="goal-unreached">
                <h2 style="text-align: center;">{goal.nombre}</h2>
                <hr>
                <h4>Tipo de Meta: {goal.tipo.upper()}</h4>
                <h4>Cantidad Meta: {goal.cantidad}</h4>
                <h4>Cantidad Informada: {informe[goal.tipo]}</h4>
                <h2 style="text-align: center;">META NO ALCANZADA</h2>
            </div>
            <br>
            """
    htmlMessage += """
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(htmlMessage, "html"))
    msg = msg.as_string()
    try:
        port = 465
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender, REPORTBOT_PASS)
            server.sendmail(sender, receiver, msg)
    except:
        raise


def envia_Avance(avance, goallist, publicador:Publicador):
    diaAvance = Dia().getFecha()
    sender = REPORTBOT_EMAIL
    receiver = publicador.correoPersonal
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Avance del Informe"
    htmlMsg = """
    <html>
    <head>
        <style>
            .tbl{
                margin-left: auto;
                margin-right: auto;
                width: 90%;
            }

            #goal-title{
                height: 70px;
                background-color: gray;
            }

            #goal-title th{
                padding-top: 3%;
                color: white;
            }

            .goal-plus #message{
                background-color: lightgreen;
            }

            .goal-less #message{
                background-color: yellow;
            }

            #message td{
                text-align: center;
                padding-left: 2%;
                padding-top: 2%;
            }

            .data td{
                text-align: center;
            }
        </style>
    </head>
    """
    htmlMsg += f"""
    <body>
        <br>
        <h1 style="text-align: center;">Avance al {diaAvance}</h1>
    <table border="3" style="background-color: wheat; width: 65%; text-align: center; margin-left: auto; margin-right: auto;">
        <tr style="height: 50px;">
            <td style="font-weight: bold;">Horas</td>
            <td style="width: 30%;">{avance['Horas']}</td>
        </tr>
        <tr style="height: 50px;">
            <td style="font-weight: bolder;">Publicaciones</td>
            <td style="width: 30%;">{avance['Publicaciones']}</td>
        </tr>
        <tr style="height: 50px;">
            <td style="font-weight: bold;">Videos</td>
            <td style="width: 30%;">{avance['Videos']}</td>
        </tr>
        <tr style="height: 50px;">
            <td style="font-weight: bold;">Revisitas</td>
            <td style="width: 30%;">{avance['Revisitas']}</td>
        </tr>
    </table>
    <br>
    <br>
    <br>
    <br>
    """
    if len(goallist) > 0:
        htmlMsg += """
        <h1 style="text-align: center;">Progreso de Metas</h1>
        <br>
        """
        for goal in goallist:
            #Este proceso no aplica para metas de Estudios
            if goal.tipo == "Estudios":
                continue
            resultados = GoalProcess.calcula_Progreso_Meta(goal, avance)
            if resultados['CantActual'] > resultados['CantEsperada']:
                htmlMsg += f"""
                <div class="goal-plus">
                    <table class="tbl" id="goal-table">
                        <tr id="goal-title">
                            <th colspan="4"><h2>{goal.nombre}</h2></th>
                        </tr>
                        <tr style="height: 45px;" class="data">
                            <td style="font-weight: bolder;">Cantidad Actual</td>
                            <td style="font-weight: bolder;">Cantidad Esperada</td>
                            <td style="font-weight: bolder;">Sobrante o faltante</td>
                            <td style="font-weight: bolder;">% de Logro</td>
                        </tr>
                        <tr style="height: 60px;" class="data">
                            <td>{resultados['CantActual']}</td>
                            <td>{resultados['CantEsperada']}</td>
                            <td>+{resultados['SobranteFaltante']}</td>
                            <td>{resultados['PorcLogro']}%</td>
                        </tr>
                        <tr id="message">
                            <td colspan="2"><h3>Excelente: Esta superando su meta</h3></td>
                            <td colspan="2" style="background-color: white;"><h3>CANTIDAD META: {goal.cantidad}</h3></td>
                        </tr>
                    </table>
                    <br>
                    <br>
                    <br>
                    <br>
                </div>
                """
            elif resultados["CantActual"] == resultados["CantEsperada"]:
                htmlMsg += f"""
                <div class="goal-plus">
                    <table class="tbl" id="goal-table">
                        <tr id="goal-title">
                            <th colspan="4"><h2>{goal.nombre}</h2></th>
                        </tr>
                        <tr style="height: 45px;" class="data">
                            <td style="font-weight: bolder;">Cantidad Actual</td>
                            <td style="font-weight: bolder;">Cantidad Esperada</td>
                            <td style="font-weight: bolder;">Sobrante o faltante</td>
                            <td style="font-weight: bolder;">% de Logro</td>
                        </tr>
                        <tr style="height: 60px;" class="data">
                            <td>{resultados['CantActual']}</td>
                            <td>{resultados['CantEsperada']}</td>
                            <td>{resultados['SobranteFaltante']}</td>
                            <td>{resultados['PorcLogro']}%</td>
                        </tr>
                        <tr id="message">
                            <td colspan="2"><h3>Muy Bien: Va igualando su meta</h3></td>
                            <td colspan="2" style="background-color: white;"><h3>CANTIDAD META: {goal.cantidad}</h3></td>
                        </tr>
                    </table>
                    <br>
                    <br>
                    <br>
                    <br>
                </div>
                """
            else:
                htmlMsg += f"""
                <div class="goal-less">
                    <table class="tbl" id="goal-table">
                        <tr id="goal-title">
                            <th colspan="4"><h2>{goal.nombre}</h2></th>
                        </tr>
                        <tr style="height: 45px;" class="data">
                            <td style="font-weight: bolder;">Cantidad Actual</td>
                            <td style="font-weight: bolder;">Cantidad Esperada</td>
                            <td style="font-weight: bolder;">Sobrante o faltante</td>
                            <td style="font-weight: bolder;">% de Logro</td>
                        </tr>
                        <tr style="height: 60px;" class="data">
                            <td>{resultados['CantActual']}</td>
                            <td>{resultados['CantEsperada']}</td>
                            <td>{resultados['SobranteFaltante']}</td>
                            <td>{resultados['PorcLogro']}%</td>
                        </tr>
                        <tr id="message">
                            <td colspan="2"><h3>Va por debajo de su meta</h3></td>
                            <td colspan="2" style="background-color: white;"><h3>CANTIDAD META: {goal.cantidad}</h3></td>
                        </tr>
                    </table>
                    <br>
                    <br>
                    <br>
                    <br>
                </div>
                """
    htmlMsg += """
        </body>
    </html>
    """

    msg.attach(MIMEText(htmlMsg, "html"))
    msg = msg.as_string()

    try:
        port = 465
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender, REPORTBOT_PASS)
            server.sendmail(sender, receiver, msg)
    except:
        raise


def send_Security_Code(publicador:Publicador, securityCode:str):
    sender = REPORTBOT_EMAIL
    reciever = publicador.correoPersonal
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = reciever
    msg['Subject'] = "Código de Seguridad"
    htmlStr = """
    <html>
    <head>
        <style>
            .big-container{
                display: block;
                margin-right: auto;
                margin-left: auto;
                width: 85%;
                border-style: hidden; 
            }
            .upper-container{
                background-color: #dcdcdc;
                margin-top: 20%;
                padding-bottom: 3%;
            }
            #programName{
                float: right;
                padding-right: 3%;
                margin-bottom: 2%;
                font-family: cursive;
            }
            #description{
                padding-left: 4%;
                padding-bottom: 2%;
            }
            #sec-code{
                text-align: center;
                font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
                font-size: 25px;
            }
        </style>
    </head>
    """
    htmlStr += f"""
    <body>
        <div class="big-container">
            <div class="upper-container">
                <aside>
                    <h2 id="programName">ReportBot</h2>
                </aside>
                <br>
                <br>
                <br>
                <h1 style="font-family: Arial, Helvetica, sans-serif; text-align: center;">Recupere su Contraseña</h1>
                <p id="description"><b>{publicador.nombreCompleto.split()[0]}</b>, 
                   usted ha solicitado cambiar su contraseña. Para hacerlo ingrese el siguiente código:
                </p>
                <h3 id="sec-code">
                    {securityCode}
                </h3>
            </div>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(htmlStr, "html"))
    msg = msg.as_string()

    try:
        port = 465
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender, REPORTBOT_PASS)
            server.sendmail(sender, reciever, msg)
    except:
        raise