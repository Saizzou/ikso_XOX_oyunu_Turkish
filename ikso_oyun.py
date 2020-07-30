import pygame as pg
import sys
import time
from pygame.locals import *

#Genel değişkenler
XO = 'x'
kazanan = None
berabere = False
width = 400 #en boyutumuz değiştirebilirsiniz
height = 400 #boy boyutumuz kare şeklinde olcak oyunumuz
cizgi = (0,0,0) #RGB şeklinde siyah çizgilerimiz olacak

#Oyun Tahtamız
tahta = [[None]*3,[None]*3,[None]*3] #Burda Liste Yöntemi ile 3er'li 3 tane alt alta sıra oluşturduk.

#Pygame Penceremizin Ayarını yapalım
pg.init() #Pygame'i çağırıp kendi içinde döndürmesini başlatıyoruz
fps = 30 #Frame Per Second Saniye başındaki resim sayısı demektir. Oyununuzun tazelenme hızıdır
saat = pg.time.Clock() # Oyunda süreyi göstermek için saat fonksiyonu.
ekran = pg.display.set_mode((width,height+100)) #Ekranın altında 100 pixellik açıklama kısmı için +100 dedik.
pg.display.set_caption("ikso Oyunu") #Ekranın en üstündeki yazımız.

#Resimlerimizi yükleyelim
anaekran = pg.image.load('ikso.png') #Projenizin olduğu dosyada olmasına dikkat etmeniz gerek
x_img = pg.image.load('ikso X.png')
o_img = pg.image.load('ikso O.png')

#Resim Boyutunu düzeltelim
x_img = pg.transform.scale(x_img, (80,80)) #400lük kutuya 3x3 yerleşebilsin önemli olan boyutu değiştirebilirsiniz
#boyutu değiştirirseniz XOciz tanımındaki hesaplarıda boyutunuza uyarlamanız gerek.
o_img = pg.transform.scale(o_img, (80,80))
anaekran = pg.transform.scale(anaekran, (width,height+100)) #Bu resmin %20 kadar uzamasına neden olacak.
#Yaparken benim gibi dikkatsiz davranmayın resmi hazırda 400x500 yapmanızı tavsiye ederim.

#Oyunun Açılışı (Ufak bir animasyon ile)
def oyun_acilis():
    ekran.blit(anaekran,(0,0))
    '''Burda aslında şunu yaptık: pygame.display.set_mode.blit ile 400x500 olan
    ana ekranımızı pygame penceremize çizdik. Burda blit çiz manasına gelir. blit komutundan önceki kodumuz ise
    ekran modunu tanımlama kodumuzdur.'''
    pg.display.update() #Ekranın güncellemesini sağlıyoruz.
    time.sleep(5) #Ekranı 1 saniyeliğine durdurup aşağıdada beyaz ile doldurcaz
    ekran.fill((255,255,255)) #Ekranın arka planını beyaz yapıyoruz.

    #Dikey çizgileri çizelim
    pg.draw.line(ekran, cizgi, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(ekran, cizgi, (width / 3*2, 0), (width / 3*2, height), 7)
    '''Burda pg.draw.line komutu ile çizgiyi çiz komutu verdik. Parantez içinde (yerini,rengini,başlangıç noktası(x,y)
    ,bitiş noktasını(x,y),kalınlık) olarak belirttik. Unutmayın rengini projenin en üstünde değişkenler kısmında
    belirttik. Başlangıç noktamız ilk kodumuzda x için: ekranın 3'te 1'i iken ikinci kodumuzda ekranın 3'te 2'sinde
    bulunmaktadır ve y ekseni 0'dan yüksekliğe kadar gidecektir'''

    #Yatay çizgileri çizelim
    pg.draw.line(ekran,cizgi,(0,height/3),(width,height/3),7)
    pg.draw.line(ekran,cizgi,(0,height/3*2),(width,height/3*2),7) #Dikey'in aynı prensibi
    durum_cubugu() #Oyun durumunu belirleyecek olan alt kısımda ayırdığımız 100px'lik kısmı çizdirecek.

def durum_cubugu():
    global berabere #Her yere ulasabilecek bir berabere tanımı.

    if kazanan is None:
        mesaj = XO.upper() + " Sırada" #.upper() büyük harf yapmak için. Bildiğinizi umuyorum ama yine belirteyim.
    else:
        mesaj = kazanan.upper() + " kazandı!"
    if berabere:
        mesaj = 'Oyun Berabere!'

    font = pg.font.Font(None,30) #Font'u belirler eğer bir font dosyanız varsa None ile değiştirin, font boyutu.
    text = font.render(mesaj,1, (255,0,0)) #Yazımızı renderliyoruz. (yazı,antialias,renk,arkaplan) olarak ayarlanır.

    #Mesaj'ı oyun tahtamıza aktaralım
    ekran.fill((0,0,0), (0,400,500,100))
    text_kutu = text.get_rect(center=(width/2, 500-50)) #Burda yazımızın kutusunun orta noktasını belirledik
    ekran.blit(text,text_kutu) #Yazımızı blit komutu ile alt kutumuza yerleştirdik.
    pg.display.update() #Güncelleme yapmazsa değişim olmayacaktır yazıda bu yüzden güncellenmesi gerek.

def kazanan_kontrol():
    '''Burda kazananı kontrol edecek bir fonksiyon oluşturacağız. Burda önemli olan X veya O hamlelerinden 3 adet yan
    yana, alt alta veya çapraz olarak oluşturulduysa oyunun durmasın sağlamak. O zaman bu fonksiyon her hamleden sonra
    çağrılması gereken bir fonksiyondur bunu unutmayalım.'''

    global tahta, kazanan, berabere

    # Kazanan Satırı Kontrol edelim
    for row in range (0,3):
        if ((tahta[row][0]==tahta[row][1]==tahta[row][2]) and (tahta[row][0] is not None)):
            kazanan = tahta[row][0]
            pg.draw.line(ekran,(255,0,0),(5,(row+1)*height/3-height/6),\
                         (width-5,(row+1)*height/3-height/6),4)
            break
    '''Evet kafalar karıştı şimdi. Burda neler yaptık bir bakalım. Şimdi kısa olsun diye Satırı row olarak
    tanıtıp bir döngüye soktum. 3 satırımız olduğu için bunu bu aralık içinde yaptık. 
            
    Eğer satır listemizde bulunan ilk [0], ikinci[1] ve üçüncü[2] elemanı aynı ise kazandı durumu olacağı için bunlar eşit ise
    diyip ilk eleman None yani boş değil ise dedik. Burda illa ilk demek zorunda değiliz 1 yada 2 de 
    diyebilirdik. Önemli olan oyuna ilk başladığımızda liste elemanlarının hepsi boş olacağı için hemen 
    başlar başlamaz bir kazanma durumu oluşmasını engellemek.
            
    Kazananı döngümüzdeki kaçıncı döngüde ise ilk eleman olarak belirttik. Yine belirteyim burda 1 veya 2 de
    diyebilirdik
            
    Kazanma durumunda üstüne bir çizgi çekilsin diye çizme komutu oluşturduk ve parantez içini (nerde, renk,
    (x,y)başlangıcı,(x,y)bitişi,kalınlık) olarak düzenledik. Hemen ekrana bitişik başlayıp bitmesin diye
    5ten başlatıp sonunda 5 çıkardım.
            
    (x,y) kısmını için: ilk x = 5 dedik ilk y = döngüdeki sayı+1 çünkü döngü 0'dan başlıyor! çarpı yükseklik
    bölü 3 eksi yükseklik bölü 6 ((y/3)-(y/6)) dan Satırın orta noktasını bulmuş oluyoruz! '''

    #Kazanan Sütunu Kontrol edelim
    for col in range(0,3):
        if ((tahta[0][col]==tahta[1][col]==tahta[2][col]) and (tahta[0][col]is not None)):
            kazanan = tahta[0][col]
            pg.draw.line(ekran,(255,0,0),((col+1)*width/3-width/6,5),\
                         ((col+1)*width/3-width/6,height-5),4)
            break

    #Kazanan Çaprazı Kontrol edelim
    if (tahta[0][0]==tahta[1][1]==tahta[2][2]) and (tahta[0][0] is not None):
        kazanan = tahta[0][0]
        pg.draw.line(ekran,(255,0,0),(50,50),(350,350),4)

    if (tahta[0][2]==tahta[1][1]==tahta[2][0]) and (tahta[0][2] is not None):
        kazanan = tahta[0][2]
        pg.draw.line(ekran,(255,0,0),(350,50),(50,350),4)

    if (all([all(row) for row in tahta]) and kazanan is None):
        berabere = True
    durum_cubugu()

def XOsec(row,col):
    global tahta, XO
    if row == 1:
        posx = 30
    if row == 2:
        posx = width/3+30
    if row == 3:
        posx = width/3*2+30

    if col == 1:
        posy = 30
    if col == 2:
        posy = height/3+30
    if col == 3:
        posy = height/3*2+30

    tahta[row-1][col-1] = XO
    if(XO == 'x'): #başlangıcı x ile yapıp sıramızı o'ya veriyoruz.
        ekran.blit(x_img,(posy,posx))

        XO= 'o'
    else: #if komutuyla o'ya sıramızı verdiğimiz için artık bu komut geçerli olacaktır if(XO =='o') olarakta yapılırdı
        #gereksiz fazla if komutu sistem şişmesine neden olmakta bu yüzden tavsiye etmem düzgün kod değildir!
        ekran.blit(o_img,(posy,posx))
        XO='x'
    pg.display.update()
    #print(posx,posy) komutu ile isterseniz terminalde hareketleri görebilirsiniz
    #print(tahta) komutu ile isterseniz tahtla Liste durumunu görebilirsiniz.

def secim(): #Yaptığımız tıklama sonucu seçim tanımımız.
    x,y = pg.mouse.get_pos() #Farenin x ve y pozisyonunu seçen komuttur.

    if(x<width/3):
        col = 1
    elif(x<width/3*2):
        col = 2
    elif(x<width):
        col = 3
    else:
        col = None

    if (y<height/3):
        row = 1
    elif (y<height/3*2):
        row = 2
    elif (y<height):
        row = 3
    else:
        row = None
    #print (row,col) satır ve sütun çıktısnı terminalde isterseniz kullanabilirsiniz.

    '''Yine bir açıklama yapalım. Şimdi programımızın penceresindeki x ve y kooordinatlarını ve yine programımızın 
    penceresinde tıkladığımız x ve y koordinatlarını kıyaslamış olacağız yukarıdaki açıklamada. Ve bu bilgileri
    de XOsec komutumuza aktaracağız.'''

    if (row and col and tahta[row-1][col-1] is None): #Burda -1 yaptık çünkü liste 0'dan başlar!
        global XO
        XOsec(row, col)
        kazanan_kontrol() #Kazananı her hamlede kontrol ettiriyoruz!

def yeniden_baslat():
    global tahta, kazanan, XO, berabere
    time.sleep(3)
    XO = 'x'
    berabere = False
    oyun_acilis()
    kazanan = None
    tahta = [[None]*3,[None]*3,[None]*3]
    #Oyunu sıfırladık

'''Oyunu başlatıp çağırma vaktimiz geldi. Sonrasında bir sonsuz döngü oluşturup faremiz ile işlem yapıp yapmadığımıza
bakacağız. Eğer bir yenme yada berabere durumu oluşursada oyunu yeniden_baslat fonksiyonu ile sıfırlayacağız. '''

oyun_acilis()
while(True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type is MOUSEBUTTONDOWN :
            secim()
            if(kazanan or berabere):
                yeniden_baslat()
    pg.display.update()
CLOCK.tick(fps)
