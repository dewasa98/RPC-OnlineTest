import xmlrpc.client
import getpass
import os
import time
from prettytable import PrettyTable

SERVER_IP = 'localhost'
SERVER_PORT = '8000'
server = xmlrpc.client.ServerProxy(
    'http://{ip}:{port}'.format(ip=SERVER_IP, port=SERVER_PORT)
)


def menu_awal():
    os.system('clear')
    t = PrettyTable(["SELAMAT DATANG DI KUIS ONLINE BAHASA INGGRIS"])
    t.align["SELAMAT DATANG DI KUIS ONLINE BAHASA INGGRIS"] = 'l'
    t.add_row(['1. Login User'])
    t.add_row(['2. Daftar User'])
    t.add_row(['0. Exit'])
    print(t)



def menu_user():
    os.system('clear')
    temp = server.get_nama_peserta(usr_user)[0]
    t = PrettyTable(["SELAMAT DATANG : "+temp])
    t.align["SELAMAT DATANG : "+temp] = 'l'
    t.add_row(['1. Mulai Kuis'])
    t.add_row(['2. Lihat Nilai'])
    t.add_row(['3. Lihat Jawaban'])
    t.add_row(['0. Log-out'])
    print(t)


while True:
    valid_admin = False
    valid_user = False
    os.system('clear')
    menu_awal()
    pilihan = eval(input('Masukan pilihan :'))
    if pilihan == 1:
        while True:
            os.system('clear')
            if valid_user==False:
                usr_user = input('Username :')
                usr_pass = getpass.getpass('Password :')
                valid_user = server.login_user(usr_user, usr_pass)
            if valid_user:
                menu_user()
                pilihan = eval(input('Masukan pilihan :'))
                if pilihan == 1:
                    os.system('clear')
                    soal = []
                    waktu_mulai = server.waktu_mulai()
                    waktu_selesai = server.waktu_selesai()
                    print("Waktu anda mulai kuis: ",time.ctime(waktu_mulai))
                    time.sleep(1)
                    print("Anda diberi waktu 10 menit")
                    time.sleep(1)
                    print("Selesaikan kuis sebelum: ",time.ctime(waktu_selesai))
                    time.sleep(1)
                    print("Kuis dimulai dalam...")
                    time.sleep(2)
                    for i in range(3,0,-1):
                        print(i)
                        time.sleep(1)
                    soal = server.get_soal()
                    jawab = []
                    num = 1
                    for i in soal :
                        os.system('clear')
                        if (time.time() > waktu_selesai):
                            print("waktu habis")
                            time.sleep(3)
                            break      
                        while True:   
                            os.system('clear')           
                            t = PrettyTable([str(num)+". "+i[1]])
                            t.align[str(num)+". "+i[1]] = 'l'
                            t.add_row(["a. %s"%i[3]])
                            t.add_row(["b. %s"%i[4]])
                            t.add_row(["c. %s"%i[5]])
                            t.add_row(["d. %s"%i[6]])
                            print(t)
                            jaw = input("masukkan jawaban(a/b/c/d) : ")
                            if (jaw == 'a') or (jaw == 'b') or (jaw == 'c') or (jaw == 'd'):
                                break
                            else :
                                print("Tidak ada opsi %s"%jaw)
                        jawab.append(jaw)
                    nilai = 0
                    print(jawab)
                    for i in range(len(jawab)) :
                        if (soal[i][2] == jawab[i]):
                            nilai += 5
                    print("Mohon tunggu sebentar...")
                    time.sleep(1)
                    print("Nilai Anda adalah : ",nilai)
                    server.upload_nilai(nilai,usr_user,usr_pass)
                    time.sleep(2)
                    print("Nilai Anda sudah diupload")
                    for i in range((len(soal)-len(jawab))):
                        jawab.append('f')
                    server.upload_soal_peserta(soal,usr_user,jawab)
                    print("Enter to lanjutkan")
                    input()

                elif pilihan == 2:
                    os.system('clear')
                    nilai = server.lihat_nilai(usr_user)[0]
                    if not nilai:
                        temp = server.get_nama_peserta(usr_user)[0]
                        print("%s, anda belum mulai kuis."%temp)
                        time.sleep(2)
                    else:
                        temp = server.get_nama_peserta(usr_user)[0]
                        print("Hai %s, nilai anda adalah = %d"% (temp,nilai))
                        print("Enter to lanjutkan")
                        input()
                elif pilihan == 3:
                    os.system('clear')
                    jawaban = server.lihat_jawaban(usr_user)
                    if not jawaban:
                        temp = server.get_nama_peserta(usr_user)[0]
                        print("%s, anda belum mulai kuis."%temp)
                        time.sleep(2)
                    else:
                        print("---Lihat Jawaban---")
                        t = PrettyTable(['Soal', 'Jawaban Anda', 'Kunci Jawaban'])
                        for isi in jawaban:
                            t.add_row(isi)
                        print(t)
                        print('Enter to lanjutkan')
                        input()
                elif pilihan == 0:
                    valid_user == False
                    print("Log Out Successful")
                    time.sleep(0.5)
                    os.system('clear')
                    break
    elif pilihan == 2:
        os.system("clear")
        t = PrettyTable(["Registrasi"])
        id = input("Masukkan id = ")
        password = getpass.getpass('Password :')
        if server.daftar(id,password):
            print("berhasil registrasi")
            time.sleep(1)
            
    elif pilihan == 0:
        print("Thank you")
        time.sleep(0.5)
        break