import requests
from bs4 import BeautifulSoup

stem = "http://www.mhra.gov.uk/Safetyinformation/Howwemonitorthesafetyofproducts/Medicines/TheYellowCardScheme/YellowCarddata/Druganalysisprints/index.htm?secLevelIndexChar="

chars = ['Aa - Ad', 'Ae - Ah', 'Ai - Al', 'Am - Ap', 'Aq - Au', 'Av - Az', 'Ba%20-%20Bd', 'Be%20-%20Bh', 'Bi%20-%20Bl', 'Bm%20-%20Bp', 'Bq%20-%20Bu', 'Bv%20-%20Bz', 'Ca%20-%20Cd', 'Ce%20-%20Ch', 'Ci%20-%20Cl', 'Cm%20-%20Cp', 'Cq%20-%20Cu', 'Cv%20-%20Cz', 'Da%20-%20Dd', 'De%20-%20Dh', 'Di%20-%20Dl', 'Dm%20-%20Dp', 'Dq%20-%20Du', 'Dv%20-%20Dz', 'Ea%20-%20Ed', 'Ee%20-%20Eh', 'Ei%20-%20El', 'Em%20-%20Ep', 'Eq%20-%20Eu', 'Ev%20-%20Ez', 'Fa%20-%20Fd', 'Fe%20-%20Fh', 'Fi%20-%20Fl', 'Fm%20-%20Fp', 'Fq%20-%20Fu', 'Fv%20-%20Fz', 'Ga%20-%20Gd', 'Ge%20-%20Gh', 'Gi%20-%20Gl', 'Gm%20-%20Gp', 'Gq%20-%20Gu', 'Gv%20-%20Gz', 'Ha%20-%20Hd', 'He%20-%20Hh', 'Hi%20-%20Hl', 'Hm%20-%20Hp', 'Hq%20-%20Hu', 'Hv%20-%20Hz', 'Ia%20-%20Id', 'Ie%20-%20Ih', 'Ii%20-%20Il', 'Im%20-%20Ip', 'Iq%20-%20Iu', 'Iv%20-%20Iz', 'Ja%20-%20Jd', 'Je%20-%20Jh', 'Ji%20-%20Jl', 'Jm%20-%20Jp', 'Jq%20-%20Ju', 'Jv%20-%20Jz', 'Ka%20-%20Kd', 'Ke%20-%20Kh', 'Ki%20-%20Kl', 'Km%20-%20Kp', 'Kq%20-%20Ku', 'Kv%20-%20Kz', 'La%20-%20Ld', 'Le%20-%20Lh', 'Li%20-%20Ll', 'Lm%20-%20Lp', 'Lq%20-%20Lu', 'Lv%20-%20Lz', 'Ma%20-%20Md', 'Me%20-%20Mh', 'Mi%20-%20Ml', 'Mm%20-%20Mp', 'Mq%20-%20Mu', 'Mv%20-%20Mz', 'Na%20-%20Nd', 'Ne%20-%20Nh', 'Ni%20-%20Nl', 'Nm%20-%20Np', 'Nq%20-%20Nu', 'Nv%20-%20Nz', 'Oa%20-%20Od', 'Oe%20-%20Oh', 'Oi%20-%20Ol', 'Om%20-%20Op', 'Oq%20-%20Ou', 'Ov%20-%20Oz', 'Pa%20-%20Pd', 'Pe%20-%20Ph', 'Pi%20-%20Pl', 'Pm%20-%20Pp', 'Pq%20-%20Pu', 'Pv%20-%20Pz', 'Qa%20-%20Qd', 'Qe%20-%20Qh', 'Qi%20-%20Ql', 'Qm%20-%20Qp', 'Qq%20-%20Qu', 'Qv%20-%20Qz', 'Ra%20-%20Rd', 'Re%20-%20Rh', 'Ri%20-%20Rl', 'Rm%20-%20Rp', 'Rq%20-%20Ru', 'Rv%20-%20Rz', 'Sa%20-%20Sd', 'Se%20-%20Sh', 'Si%20-%20Sl', 'Sm%20-%20Sp', 'Sq%20-%20Su', 'Sv%20-%20Sz', 'Ta%20-%20Td', 'Te%20-%20Th', 'Ti%20-%20Tl', 'Tm%20-%20Tp', 'Tq%20-%20Tu', 'Tv%20-%20Tz', 'Ua%20-%20Ud', 'Ue%20-%20Uh', 'Ui%20-%20Ul', 'Um%20-%20Up', 'Uq%20-%20Uu', 'Uv%20-%20Uz', 'Va%20-%20Vd', 'Ve%20-%20Vh', 'Vi%20-%20Vl', 'Vm%20-%20Vp', 'Vq%20-%20Vu', 'Vv%20-%20Vz', 'Wa%20-%20Wd', 'We%20-%20Wh', 'Wi%20-%20Wl', 'Wm%20-%20Wp', 'Wq%20-%20Wu', 'Wv%20-%20Wz', 'Xa%20-%20Xd', 'Xe%20-%20Xh', 'Xi%20-%20Xl', 'Xm%20-%20Xp', 'Xq%20-%20Xu', 'Xv%20-%20Xz', 'Ya%20-%20Yd', 'Ye%20-%20Yh', 'Yi%20-%20Yl', 'Ym%20-%20Yp', 'Yq%20-%20Yu', 'Yv%20-%20Yz', 'Za%20-%20Zd', 'Ze%20-%20Zh', 'Zi%20-%20Zl', 'Zm%20-%20Zp', 'Zq%20-%20Zu', 'Zv%20-%20Zz'] + ['0-9']
pages = []

for char in chars:
    url = stem + char
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    options = soup.find_all("option")
    if options:
        print char, options[-1]
        max_page = options[-1]["value"]
    else:
        max_page = 0
    pages.append(int(max_page))
print zip(chars,pages)

