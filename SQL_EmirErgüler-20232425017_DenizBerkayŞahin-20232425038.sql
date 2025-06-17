CREATE DATABASE StokTakip; 
/*ilk üstteki  kod çalýþtýrýlmalý.*/

USE StokTakip;
CREATE TABLE Urunler (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Isim NVARCHAR(100) NOT NULL,     
    Fiyat INT NOT NULL,            
    Adet INT NOT NULL);               


CREATE TABLE Kullanicilar (
    KullaniciID INT IDENTITY(1,1) PRIMARY KEY,
    KullaniciAdi NVARCHAR(50) NOT NULL UNIQUE, 
    Sifre NVARCHAR(50) NOT NULL              
);
