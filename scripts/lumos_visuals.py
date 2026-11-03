"""Conceptual vector illustrations, not model-specific construction diagrams."""
from html import escape

LABELS = {
 'pl': [('Parametry impulsu','Moc głowicy','Energia','Częstotliwość'),('ICE Flow','Kontrola temperatury','Chłodzenie','Konserwacja'),('FAC','Emisja','Kolimacja','Wiązka'),('NeoDez','Higiena głowicy','Czyszczenie','Procedury'),('Android · CRM','Ustawienia','Informacje','Obserwacja skóry')],
 'en': [('Pulse settings','Handpiece power','Energy','Frequency'),('ICE Flow','Temperature management','Cooling','Maintenance'),('FAC','Emission','Collimation','Beam'),('NeoDez','Handpiece hygiene','Cleaning','Procedures'),('Android · CRM','Settings','Records','Skin observation')],
 'ru': [('Параметры импульса','Мощность манипулы','Энергия','Частота'),('ICE Flow','Контроль температуры','Охлаждение','Обслуживание'),('FAC','Излучение','Коллимация','Пучок'),('NeoDez','Гигиена манипулы','Очистка','Процедуры'),('Android · CRM','Настройки','Данные','Наблюдение кожи')]
}
ART = [
 # Pulse controls: qualitative plot, no fabricated axes or waveform values.
 '<rect x="65" y="70" width="470" height="300" rx="12" class="panel"/><path d="M100 130h400M100 200h400M100 270h400M100 340h400" class="grid"/><path d="M100 310h48v-120h65v120h55V150h65v160h55V115h65v195h47" class="beam"/><circle cx="148" cy="190" r="6" class="dot"/><circle cx="268" cy="150" r="6" class="dot"/><circle cx="388" cy="115" r="6" class="dot"/><path d="M100 395h400" class="line"/><circle cx="350" cy="395" r="13" class="knob"/>',
 # Cooling concept, deliberately not a plumbing circuit.
 '<circle cx="300" cy="220" r="155" class="halo"/><circle cx="300" cy="220" r="115" class="ring"/><path d="M300 115v210M209 167l182 106M209 273l182-106M300 115l-19 22m19-22 19 22M300 325l-19-22m19 22 19-22M209 167l29-5m-29 5 10 28M391 273l-29 5m29-5-10-28M209 273l10-28m-10 28 29 5M391 167l-10 28m10-28-29-5" class="beam"/><path d="M457 95v192a33 33 0 1 1-38 0V95a19 19 0 0 1 38 0Z" class="panel"/><path d="M438 145v160" class="beam"/><circle cx="438" cy="315" r="15" class="dot"/><path d="M105 350h120M105 380h175" class="line"/>',
 # Fast-axis collimation: source, diverging rays, conceptual lens, parallel rays.
 '<path d="M75 225h450" class="grid"/><rect x="55" y="182" width="70" height="86" rx="8" class="panel"/><circle cx="125" cy="225" r="8" class="dot"/><path d="M125 225 300 110h230M125 225 300 168h230M125 225h405M125 225 300 282h230M125 225 300 340h230" class="beam"/><ellipse cx="300" cy="225" rx="28" ry="148" class="lens"/><path d="M78 395h170m100 0h170" class="line"/><path d="m236 387 12 8-12 8m270-16 12 8-12 8" class="line"/>',
 # Hygiene: generic handpiece symbol and procedural checklist, no UV/sterilisation claim.
 '<path d="M195 75 320 120v105c0 85-50 125-125 163C120 350 70 310 70 225V120Z" class="halo"/><g transform="rotate(-25 195 220)"><rect x="157" y="135" width="76" height="174" rx="24" class="panel"/><rect x="167" y="115" width="56" height="40" rx="5" class="lens"/><path d="M195 309v56" class="line"/><circle cx="195" cy="203" r="9" class="dot"/></g><rect x="355" y="120" width="180" height="230" rx="12" class="panel"/><path d="m376 172 9 9 17-23m-26 76 9 9 17-23m-26 76 9 9 17-23" class="beam"/><path d="M424 173h82m-82 62h82m-82 62h82" class="line"/>',
 # Abstract software interface, not a Lumos screenshot or medical result.
 '<rect x="55" y="65" width="490" height="310" rx="14" class="panel"/><path d="M55 112h490" class="grid"/><circle cx="83" cy="88" r="5" class="dot"/><circle cx="103" cy="88" r="5" class="dot"/><path d="M240 375v35m120-35v35M205 410h190" class="line"/><rect x="85" y="142" width="200" height="200" rx="8" class="halo"/><path d="M110 185h150m-150 55h150m-150 55h150" class="line"/><circle cx="160" cy="185" r="10" class="knob"/><circle cx="222" cy="240" r="10" class="knob"/><circle cx="185" cy="295" r="10" class="knob"/><circle cx="342" cy="172" r="20" class="lens"/><path d="M313 225c0-40 58-40 58 0M397 157h113m-113 25h85m-85 25h100" class="line"/><circle cx="413" cy="287" r="43" class="ring"/><path d="m444 318 30 30" class="beam"/><circle cx="400" cy="280" r="5" class="dot"/><circle cx="425" cy="297" r="7" class="dot"/>'
]

def illustration(lang, index):
    labels=LABELS[lang][index]
    note={'pl':'Schemat poglądowy technologii','en':'Conceptual technology illustration','ru':'Условная схема технологии'}[lang]
    values=[['2000–4000 W','10–240 J','1–30 Hz'],['ICE Flow','ICE Flow','ICE Flow'],['01','02','03'],['01','02','03'],['Android','CRM','03']][index]
    # Use text labels alone where a numerical metric is not established.
    metrics=''.join('<div><strong>'+escape(values[i] if index==0 else labels[i+1])+'</strong>'+('<span>'+escape(labels[i+1])+'</span>' if index==0 else '')+'</div>' for i in range(3))
    return f'<figure class="lumos-diagram"><div class="lumos-diagram__heading"><span>LUMOS / 0{index+1}</span><strong>{escape(labels[0])}</strong></div><svg viewBox="0 0 600 460" aria-hidden="true" focusable="false">{ART[index]}</svg><div class="lumos-diagram__metrics">{metrics}</div><figcaption>{escape(note)}</figcaption></figure>'


def wavelength_illustration(lang):
    """Four qualitative waves; no tissue depths or relative efficacy implied."""
    from math import sin, pi
    title={'pl':'Cztery długości fal','en':'Four wavelengths','ru':'Четыре длины волны'}[lang]
    note={'pl':'Schemat poglądowy fal. Nie przedstawia głębokości działania w skórze.', 'en':'Conceptual wave illustration. Does not represent penetration depth in skin.', 'ru':'Условная схема волн. Не показывает глубину воздействия в коже.'}[lang]
    unit='нм' if lang=='ru' else 'nm'
    rows=[]
    for i, wavelength in enumerate([755,808,940,1064]):
        y=35+i*155
        points=' '.join(f'{x:.1f},{y+84+25*sin(2*pi*(x-55)/(wavelength/8)):.1f}' for x in range(55,546,3))
        rows.append(f'<rect x="25" y="{y}" width="550" height="135" rx="8" class="panel"/><text x="55" y="{y+34}" fill="currentColor" font-size="23" font-weight="600">{wavelength} {unit}</text><path d="M55 {y+84}h490" class="grid"/><polyline points="{points}" class="beam"/>')
    return f'<figure class="lumos-diagram"><div class="lumos-diagram__heading"><span>LUMOS / λ</span><strong>{escape(title)}</strong></div><svg viewBox="0 0 600 660" aria-hidden="true" focusable="false">{"".join(rows)}</svg><div class="lumos-diagram__metrics"><strong>755 / 808 / 940 / 1064 {unit}</strong></div><figcaption>{escape(note)}</figcaption></figure>'
