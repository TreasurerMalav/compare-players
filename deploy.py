from flask import Flask, render_template, request, url_for, redirect, flash
from flask_wtf import FlaskForm 
import requests
import bs4

app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = 'secret'


players = [{"Name":"Virat Kohli(IND)","url":"http://www.espncricinfo.com/india/content/player/253802.html"},
{"Name":"MS Dhoni(IND)","url":"http://www.espncricinfo.com/india/content/player/28081.html"},
{"Name":"Rohit Sharma(IND)","url":"http://www.espncricinfo.com/india/content/player/34102.html"},
{"Name":"Shikhar Dhawan(IND)","url":"http://www.espncricinfo.com/india/content/player/28235.html"},
{"Name":"KL Rahul(IND)","url":"http://www.espncricinfo.com/india/content/player/422108.html"},
{"Name":"Hardik Pandya(IND)","url":"http://www.espncricinfo.com/india/content/player/625371.html"},
{"Name":"Ravindra Jadeja(IND)","url":"http://www.espncricinfo.com/india/content/player/234675.html"},
{"Name":"Bhuvneshwar Kumar(IND)","url":"http://www.espncricinfo.com/india/content/player/326016.html"},
{"Name":"Mohammed Shami(IND)","url":"http://www.espncricinfo.com/india/content/player/481896.html"},
{"Name":"Jasprit Bumrah(IND)","url":"http://www.espncricinfo.com/india/content/player/625383.html"},
{"Name":"Yuzvendra Chahal(IND)","url":"http://www.espncricinfo.com/india/content/player/430246.html"},
{"Name":"Vijay Shankar(IND)","url":"http://www.espncricinfo.com/india/content/player/477021.html"},
{"Name":"Kedar Jadhav(IND)","url":"http://www.espncricinfo.com/india/content/player/290716.html"},
{"Name":"Kuldeep Yadav(IND)","url":"http://www.espncricinfo.com/india/content/player/559235.html"},
{"Name":"Dinesh Karthik(IND)","url":"http://www.espncricinfo.com/india/content/player/30045.html"},
{"Name":"Eoin Morgan(ENG)","url":"http://www.espncricinfo.com/england/content/player/24598.html"},
{"Name":"Jason Roy(ENG)","url":"http://www.espncricinfo.com/england/content/player/298438.html"},
{"Name":"Joony Baristow(ENG)","url":"http://www.espncricinfo.com/england/content/player/297433.html"},
{"Name":"James Vince(ENG)","url":"http://www.espncricinfo.com/england/content/player/296597.html"},
{"Name":"Jos Buttler(ENG)","url":"http://www.espncricinfo.com/england/content/player/308967.html"},
{"Name":"Ben Stokes(ENG)","url":"http://www.espncricinfo.com/england/content/player/311158.html"},
{"Name":"Moeen Ali(ENG)","url":"http://www.espncricinfo.com/england/content/player/8917.html"},
{"Name":"Chris Wokes(ENG)","url":"http://www.espncricinfo.com/england/content/player/247235.html"},
{"Name":"Liam Dawson(ENG)","url":"http://www.espncricinfo.com/england/content/player/211855.html"},
{"Name":"Tom Curran(ENG)","url":"http://www.espncricinfo.com/england/content/player/550235.html"},
{"Name":"Liam Plunkett(ENG)","url":"http://www.espncricinfo.com/england/content/player/19264.html"},
{"Name":"Mark Wood(ENG)","url":"http://www.espncricinfo.com/england/content/player/351588.html"},
{"Name":"Adil Rashid(ENG)","url":"http://www.espncricinfo.com/england/content/player/244497.html"},
{"Name":"Jofra Archer(ENG)","url":"http://www.espncricinfo.com/westindies/content/player/669855.html"},
{"Name":"Joe Root(ENG)","url":"http://www.espncricinfo.com/england/content/player/303669.html"},
{"Name":"Kane Williamson(NZ)","url":"http://www.espncricinfo.com/newzealand/content/player/277906.html"},
{"Name":"Trent Boult(NZ)","url":"http://www.espncricinfo.com/newzealand/content/player/277912.html"},
{"Name":"Lockie Fergusion(NZ)","url":"http://www.espncricinfo.com/newzealand/content/player/493773.html"},
{"Name":"Matt Henry(NZ)","url":"http://www.espncricinfo.com/newzealand/content/player/506612.html"},
{"Name":"Colin Munro(NZ)","url":"http://www.espncricinfo.com/newzealand/content/player/232359.html"},
{"Name":"Henry Nicholls(NZ)","url":"http://www.espncricinfo.com/newzealand/content/player/539511.html"},
{"Name":"Ish Sodhi(NZ)","url":"http://www.espncricinfo.com/newzealand/content/player/559066.html"},
{"Name":"Ross Taylor(NZ)","url":"http://www.espncricinfo.com/newzealand/content/player/38699.html"},
{"Name":"Tom Blundell(NZ)","url":"http://www.espncricinfo.com/newzealand/content/player/440516.html"},
{"Name":"Colin de Grandhomme(NZ)","url":"http://www.espncricinfo.com/newzealand/content/player/55395.html"},
{"Name":"Martin Guptil(NZ)","url":"http://www.espncricinfo.com/newzealand/content/player/226492.html"},
{"Name":"Tom Latham(NZ)","url":"http://www.espncricinfo.com/newzealand/content/player/388802.html"},
{"Name":"James Neesham","url":"http://www.espncricinfo.com/newzealand/content/player/355269.html"},
{"Name":"Mitchell Santner(NZ)","url":"http://www.espncricinfo.com/newzealand/content/player/502714.html"},
{"Name":"Tim Southee(NZ)","url":"http://www.espncricinfo.com/newzealand/content/player/232364.html"},
{"Name":"Faf du Plessis(SA)","url":"http://www.espncricinfo.com/ci/content/player/44828.html"},
{"Name":"Hashim Amla(SA)","url":"http://www.espncricinfo.com/ci/content/player/43906.html"},
{"Name":"Quinton de Kock(SA)","url":"http://www.espncricinfo.com/ci/content/player/379143.html"},
{"Name":"Imran Tahir(SA)","url":"http://www.espncricinfo.com/ci/content/player/40618.html"},
{"Name":"Jean-Paul Duminy(SA)","url":"http://www.espncricinfo.com/ci/content/player/44932.html"},
{"Name":"Aiden Markram(SA)","url":"http://www.espncricinfo.com/ci/content/player/600498.html"},
{"Name":"David Miller(SA)","url":"http://www.espncricinfo.com/ci/content/player/321777.html"},
{"Name":"Chris Morris(SA)","url":"http://www.espncricinfo.com/ci/content/player/439952.html"},
{"Name":"Lungi Ngidi(SA)","url":"http://www.espncricinfo.com/ci/content/player/542023.html"},
{"Name":"Andile Phehlukwayo(SA)","url":"http://www.espncricinfo.com/ci/content/player/540316.html"},
{"Name":"Dwaine Pretorius(SA)","url":"http://www.espncricinfo.com/ci/content/player/327830.html"},
{"Name":"Kagiso Rabada(SA)","url":"http://www.espncricinfo.com/ci/content/player/550215.html"},
{"Name":"Tabraiz Shamsi(SA)","url":"http://www.espncricinfo.com/ci/content/player/379145.html"},
{"Name":"Dale Steyn(SA)","url":"http://www.espncricinfo.com/ci/content/player/47492.html"},
{"Name":"Rassie van der Dussen(SA)","url":"http://www.espncricinfo.com/ci/content/player/337790.html"},
{"Name":"Anrich Nortje(SA)","url":"http://www.espncricinfo.com/ci/content/player/481979.html"},
{"Name":"Aaron Finch(AUS)","url":"http://www.espncricinfo.com/australia/content/player/5334.html"},
{"Name":"David Warner(AUS)","url":"http://www.espncricinfo.com/australia/content/player/219889.html"},
{"Name":"Usman Khawaja(AUS)","url":"http://www.espncricinfo.com/australia/content/player/215155.html"},
{"Name":"Steven Smith(AUS)","url":"http://www.espncricinfo.com/australia/content/player/267192.html"},
{"Name":"Shaun Marsh(AUS)","url":"http://www.espncricinfo.com/australia/content/player/6683.html"},
{"Name":"Marcus Stoinis(AUS)","url":"http://www.espncricinfo.com/australia/content/player/325012.html"},
{"Name":"Alex Carey(AUS)","url":"http://www.espncricinfo.com/australia/content/player/326434.html"},
{"Name":"Nathan Coulter-Nile(AUS)","url":"http://www.espncricinfo.com/australia/content/player/261354.html"},
{"Name":"Jason Behrendroff(AUS)","url":"http://www.espncricinfo.com/australia/content/player/272477.html"},
{"Name":"Kane Richardson(AUS)","url":"http://www.espncricinfo.com/australia/content/player/272262.html"},
{"Name":"Nathan Lyon(AUS)","url":"http://www.espncricinfo.com/australia/content/player/272279.html"},
{"Name":"Adam Zampa(AUS)","url":"http://www.espncricinfo.com/australia/content/player/379504.html"},
{"Name":"Glenn Maxwell(AUS)","url":"http://www.espncricinfo.com/australia/content/player/325026.html"},
{"Name":"Mitchell Starc(AUS)","url":"http://www.espncricinfo.com/australia/content/player/311592.html"},
{"Name":"Pat Cummins(AUS)","url":"http://www.espncricinfo.com/australia/content/player/489889.html"},
{"Name":"Jason Holder(WI)","url":"http://www.espncricinfo.com/westindies/content/player/391485.html"},
{"Name":"Evin Lewis(WI)","url":"http://www.espncricinfo.com/westindies/content/player/431901.html"},
{"Name":"Darren Bravo(WI)","url":"http://www.espncricinfo.com/westindies/content/player/277472.html"},
{"Name":"Chris Gayle(WI)","url":"http://www.espncricinfo.com/westindies/content/player/51880.html"},
{"Name":"Andre Russell(WI)","url":"http://www.espncricinfo.com/westindies/content/player/276298.html"},
{"Name":"Carlos Brathwaite(WI)","url":"http://www.espncricinfo.com/westindies/content/player/457249.html"},
{"Name":"Nicholas Pooran(WI)","url":"http://www.espncricinfo.com/westindies/content/player/604302.html"},
{"Name":"Oshane Thomas(WI)","url":"http://www.espncricinfo.com/westindies/content/player/914567.html"},
{"Name":"Shai Hope(WI)","url":"http://www.espncricinfo.com/westindies/content/player/581379.html"},
{"Name":"Shimron Hetmyer(WI)","url":"http://www.espncricinfo.com/westindies/content/player/670025.html"},
{"Name":"Fabien Allen(WI)","url":"http://www.espncricinfo.com/westindies/content/player/670013.html"},
{"Name":"Sheldon Cottrell(WI)","url":"http://www.espncricinfo.com/westindies/content/player/495551.html"},
{"Name":"Shannon Gabriel(WI)","url":"http://www.espncricinfo.com/westindies/content/player/446101.html"},
{"Name":"Kemar Roach(WI)","url":"http://www.espncricinfo.com/westindies/content/player/230553.html"},
{"Name":"Ashley Nurse(WI)","url":"http://www.espncricinfo.com/westindies/content/player/315594.html"},
{"Name":"Shoaib Malik(PAK)","url":"http://www.espncricinfo.com/pakistan/content/player/42657.html"},
{"Name":"Mohammad Hafeez(PAK)","url":"http://www.espncricinfo.com/pakistan/content/player/41434.html"},
{"Name":"Sarfaraz Ahmed(PAK)","url":"http://www.espncricinfo.com/pakistan/content/player/227760.html"},
{"Name":"Wahab Riaz(PAK)","url":"http://www.espncricinfo.com/pakistan/content/player/43590.html"},
{"Name":"Mohammad Amir(PAK)","url":"http://www.espncricinfo.com/pakistan/content/player/290948.html"},
{"Name":"Haris Sohail(PAK)","url":"http://www.espncricinfo.com/pakistan/content/player/318788.html"},
{"Name":"Babar Azam(PAK)","url":"http://www.espncricinfo.com/pakistan/content/player/348144.html"},
{"Name":"Imam-ul-Haq(PAK)","url":"http://www.espncricinfo.com/pakistan/content/player/568276.html"},
{"Name":"Asif Ali(PAK)","url":"http://www.espncricinfo.com/pakistan/content/player/494230.html"},
{"Name":"Imad Wasim(PAK)","url":"http://www.espncricinfo.com/pakistan/content/player/227758.html"},
{"Name":"Fakhar Zaman(PAK)","url":"http://www.espncricinfo.com/pakistan/content/player/512191.html"},
{"Name":"Shadab Khan(PAK)","url":"http://www.espncricinfo.com/pakistan/content/player/922943.html"},
{"Name":"Hasan Ali(PAK)","url":"http://www.espncricinfo.com/pakistan/content/player/681305.html"},
{"Name":"Saheen Afridi(PAK)","url":"http://www.espncricinfo.com/pakistan/content/player/1072470.html"},
{"Name":"Mohammad Hasnain(PAK)","url":"http://www.espncricinfo.com/pakistan/content/player/1158100.html"},
{"Name":"Dimuth Karunaratne(SL)","url":"http://www.espncricinfo.com/srilanka/content/player/227772.html"},
{"Name":"Angelo Mathews(SL)","url":"http://www.espncricinfo.com/srilanka/content/player/49764.html"},
{"Name":"Thisara Perera(SL)","url":"http://www.espncricinfo.com/srilanka/content/player/233514.html"},
{"Name":"Kusal Perera(SL)","url":"http://www.espncricinfo.com/srilanka/content/player/300631.html"},
{"Name":"Dhananjaya de Silva(SL)","url":"http://www.espncricinfo.com/srilanka/content/player/465793.html"},
{"Name":"Kusal Mendis(SL)","url":"http://www.espncricinfo.com/srilanka/content/player/629074.html"},
{"Name":"Isuru Udana(SL)","url":"http://www.espncricinfo.com/srilanka/content/player/328026.html"},
{"Name":"Milinda Siriwardana(SL)","url":"http://www.espncricinfo.com/srilanka/content/player/222354.html"},
{"Name":"Aviskha Fernando(SL)","url":"http://www.espncricinfo.com/srilanka/content/player/784369.html"},
{"Name":"Jeevan Mendis(SL)","url":"http://www.espncricinfo.com/srilanka/content/player/49700.html"},
{"Name":"Lahiru Thirimanne(SL)","url":"http://www.espncricinfo.com/srilanka/content/player/301236.html"},
{"Name":"Jeffrey Vandersay(SL)","url":"http://www.espncricinfo.com/srilanka/content/player/370040.html"},
{"Name":"Lasith Malinga(SL)","url":"http://www.espncricinfo.com/srilanka/content/player/49758.html"},
{"Name":"Nuwan Pradeep(SL)","url":"http://www.espncricinfo.com/srilanka/content/player/324358.html"},
{"Name":"Suranga Lakmal(SL)","url":"http://www.espncricinfo.com/srilanka/content/player/49619.html"},
{"Name":"Mashrafe Mortaza(BAN)","url":"http://www.espncricinfo.com/bangladesh/content/player/56007.html"},
{"Name":"Tamim Iqbal(BAN)","url":"http://www.espncricinfo.com/bangladesh/content/player/56194.html"},
{"Name":"Liton Das(BAN)","url":"http://www.espncricinfo.com/bangladesh/content/player/536936.html"},
{"Name":"Soumya Sarkar(BAN)","url":"http://www.espncricinfo.com/bangladesh/content/player/436677.html"},
{"Name":"Mushfiqur Rahim(BAN)","url":"http://www.espncricinfo.com/bangladesh/content/player/56029.html"},
{"Name":"Mahmudullah Riyad(BAN)","url":"http://www.espncricinfo.com/bangladesh/content/player/56025.html"},
{"Name":"Shakib Al Hasan(BAN)","url":"http://www.espncricinfo.com/bangladesh/content/player/56143.html"},
{"Name":"Mohammad Mithun(BAN)","url":"http://www.espncricinfo.com/bangladesh/content/player/269237.html"},
{"Name":"Sabbir Rahman(BAN)","url":"http://www.espncricinfo.com/bangladesh/content/player/373538.html"},
{"Name":"Mosaddek Hossain(BAN)","url":"http://www.espncricinfo.com/bangladesh/content/player/550133.html"},
{"Name":"Mohammad Saifuddin(BAN)","url":"http://www.espncricinfo.com/bangladesh/content/player/629070.html"},
{"Name":"Mehidy Hasan(BAN)","url":"http://www.espncricinfo.com/bangladesh/content/player/629063.html"},
{"Name":"Rubel Hossain(BAN)","url":"http://www.espncricinfo.com/bangladesh/content/player/300619.html"},
{"Name":"Mustafizur Rahman(BAN)","url":"http://www.espncricinfo.com/bangladesh/content/player/330902.html"},
{"Name":"Abu Jayed(BAN)","url":"http://www.espncricinfo.com/bangladesh/content/player/410763.html"},
{"Name":"Gulbadin Naib(AFG)","url":"http://www.espncricinfo.com/afghanistan/content/player/352048.html"},
{"Name":"Mohammad Shahzad(AFG)","url":"http://www.espncricinfo.com/afghanistan/content/player/419873.html"},
{"Name":"Noor Ali Zardan(AFG)","url":"http://www.espncricinfo.com/afghanistan/content/player/318340.html"},
{"Name":"Hazratullah Zazai(AFG)","url":"http://www.espncricinfo.com/afghanistan/content/player/793457.html"},
{"Name":"Rahmat Shah(AFG)","url":"http://www.espncricinfo.com/afghanistan/content/player/533956.html"},
{"Name":"Asghar Afghan(AFG)","url":"http://www.espncricinfo.com/afghanistan/content/player/320652.html"},
{"Name":"Hashmatullah Shahidi(AFG)","url":"http://www.espncricinfo.com/afghanistan/content/player/440970.html"},
{"Name":"Najibullah Zardan(AFG)","url":"http://www.espncricinfo.com/afghanistan/content/player/524049.html"},
{"Name":"Samiullah Shinwari(AFG)","url":"http://www.espncricinfo.com/afghanistan/content/player/318339.html"},
{"Name":"Mohammad Nabi(AFG)","url":"http://www.espncricinfo.com/afghanistan/content/player/25913.html"},
{"Name":"Rashid Khan(AFG)","url":"http://www.espncricinfo.com/afghanistan/content/player/793463.html"},
{"Name":"Dawalat Zardan(AFG)","url":"http://www.espncricinfo.com/afghanistan/content/player/516561.html"},
{"Name":"Aftab Alam(AFG)","url":"http://www.espncricinfo.com/afghanistan/content/player/440963.html"},
{"Name":"Hamid Hassan(AFG)","url":"http://www.espncricinfo.com/afghanistan/content/player/311427.html"},
{"Name":"Mujeeb ur Rahman(AFG)","url":"http://www.espncricinfo.com/afghanistan/content/player/974109.html"}]

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        player1 = request.form.get('players')
        player2 = request.form.get('players2')
        return redirect(url_for('compare', player1=player1, player2=player2))

        #return "<p style='margin-left:200px'>" + "<b>" + player1 + "</b>" +  "<br><br>" +"<u><b>Batting and Fielding Performance</b></u>" + "<br><b>Matches:</b> " + matches + "<br><b>Innings:</b> " + innings + "<br><b>NotOuts:</b> " + notouts + "<br><b>Runs:</b> " + runs + "<br><b>Highest:</b> " + highest + "<br><b>Average:</b> " + average + "<br><b>Balls Faced:</b> " + bf + "<br><b>Strike Rate:</b> " + sr + "<br><b>100s:</b> " + hundreds + "<br><b>50s:</b> " + fifties + "<br><b>Catches:</b> " + catches + "<br><b>Stumpings:</b> " + stumpings + "<br><br>" + "<u><b>Bowling Performance</b></u>" + "<br><b>Matches:</b> " + matchesb + "<br><b>Innings:</b> " + inningsb + "<br><b>Wickets:</b> " + wickets + "<br><b>Best Bowling Figure:</b> " + bestb + "<br><b>Bowling Average:</b> " + averageb + "<br><b>Economy:</b> " + economy + "<br><b>Bowling Strike Rate:</b> " + srb + "<br><b>5 Wickets Haul:</b> " + fwkt + "<br><br>" + player2 + matches2 + "</p>"
        
    return render_template('index.html', players=players)

@app.route('/compare/<player1>/<player2>')
def compare(player1, player2):
    for i in players:
        a = players.index(i)
        if players[a].get('Name') == player1:
            my_url = players[a].get("url")
            res = requests.get(my_url)
            soup = bs4.BeautifulSoup(res.text,"html.parser")
            ti = soup.select('.engineTable')
            ti1 = ti[0].select('tbody')
            ti2 = ti1[0].select('tr')
            ti3 = ti2[1].select('td')
            temp1 = ti3[0].getText()
            if temp1 == "ODIs":
                matches = ti3[1].getText()
                innings = ti3[2].getText()
                notouts = ti3[3].getText()
                runs = ti3[4].getText()
                highest = ti3[5].getText()
                average = ti3[6].getText()
                bf = ti3[7].getText()
                sr = ti3[8].getText()
                hundreds = ti3[9].getText()
                fifties = ti3[10].getText()
                catches = ti3[13].getText()
                stumpings = ti3[14].getText()
            else:
                ti3 = ti2[0].select('td')
                matches = ti3[1].getText()
                innings = ti3[2].getText()
                notouts = ti3[3].getText()
                runs = ti3[4].getText()
                highest = ti3[5].getText()
                average = ti3[6].getText()
                bf = ti3[7].getText()
                sr = ti3[8].getText()
                hundreds = ti3[9].getText()
                fifties = ti3[10].getText()
                catches = ti3[13].getText()
                stumpings = ti3[14].getText()

            ti4 = ti[1].select('tbody')
            ti5 = ti4[0].select('tr')
            ti6 = ti5[1].select('td')
            temp3 = ti6[0].getText()
            if temp3 == "ODIs":
                inningsb = ti6[2].getText()
                wickets = ti6[5].getText()
                bestb = ti6[7].getText()
                averageb = ti6[8].getText()
                economy = ti6[9].getText()
                srb = ti6[10].getText()
                fwkt = ti6[12].getText()
            else:
                ti6 = ti5[0].select('td')
                inningsb = ti6[2].getText()
                wickets = ti6[5].getText()
                bestb = ti6[7].getText()
                averageb = ti6[8].getText()
                economy = ti6[9].getText()
                srb = ti6[10].getText()
                fwkt = ti6[12].getText()
            break

    for i in players:
        a = players.index(i)
        if players[a].get('Name') == player2:
            my_url = players[a].get("url")
            res = requests.get(my_url)
            soup = bs4.BeautifulSoup(res.text,"html.parser")
            ti = soup.select('.engineTable')
            ti1 = ti[0].select('tbody')
            ti2 = ti1[0].select('tr')
            ti3 = ti2[1].select('td')
            temp2 = ti3[0].getText()
            if temp2 == "ODIs":
                matches2 = ti3[1].getText()
                innings2 = ti3[2].getText()
                notouts2 = ti3[3].getText()
                runs2 = ti3[4].getText()
                highest2 = ti3[5].getText()
                average2 = ti3[6].getText()
                bf2 = ti3[7].getText()
                sr2 = ti3[8].getText()
                hundreds2 = ti3[9].getText()
                fifties2 = ti3[10].getText()
                catches2 = ti3[13].getText()
                stumpings2 = ti3[14].getText()
            else:
                ti3 = ti2[0].select('td')
                matches2 = ti3[1].getText()
                innings2 = ti3[2].getText()
                notouts2 = ti3[3].getText()
                runs2 = ti3[4].getText()
                highest2 = ti3[5].getText()
                average2 = ti3[6].getText()
                bf2 = ti3[7].getText()
                sr2 = ti3[8].getText()
                hundreds2 = ti3[9].getText()
                fifties2 = ti3[10].getText()
                catches2 = ti3[13].getText()
                stumpings2 = ti3[14].getText()

            ti4 = ti[1].select('tbody')
            ti5 = ti4[0].select('tr')
            ti6 = ti5[1].select('td')
            temp4 = ti6[0].getText()
            if temp4 == "ODIs":
                inningsb2 = ti6[2].getText()
                wickets2 = ti6[5].getText()
                bestb2 = ti6[7].getText()
                averageb2 = ti6[8].getText()
                economy2 = ti6[9].getText()
                srb2 = ti6[10].getText()
                fwkt2 = ti6[12].getText()
            else:
                ti6 = ti5[0].select('td')
                inningsb2 = ti6[2].getText()
                wickets2 = ti6[5].getText()
                bestb2 = ti6[7].getText()
                averageb2 = ti6[8].getText()
                economy2 = ti6[9].getText()
                srb2 = ti6[10].getText()
                fwkt2 = ti6[12].getText()
                
    return render_template('index3.html', player1=player1, player2=player2, matches=matches, matches2=matches2, innings=innings, innings2=innings2, notouts=notouts, notouts2=notouts2, runs=runs, runs2=runs2, highest=highest, highest2=highest2, average=average, average2=average2, bf=bf, bf2=bf2, sr=sr, sr2=sr2, hundreds=hundreds, hundreds2=hundreds2, fifties=fifties, fifties2=fifties2, stumpings=stumpings, stumpings2=stumpings2, catches=catches, catches2=catches2, inningsb=inningsb, inningsb2=inningsb2, wickets=wickets, wickets2=wickets2, bestb=bestb, bestb2=bestb2, averageb=averageb, averageb2=averageb2, economy=economy, economy2=economy2, srb=srb, srb2=srb2, fwkt=fwkt, fwkt2=fwkt2)

    #return "You are at compare page." + str(player1) + str(player2)

if __name__ == "__main__":
    app.run()
