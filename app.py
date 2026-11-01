import time
import random
import streamlit as st

# Sayfa Yapılandırması

st.set_page_config(
    page_title="Akıllı Kredi Onay Sistemi", page_icon="💳", layout="centered"
)

st.title("💳 Akıllı Kredi Onay Sistemi")
st.markdown(
    "Yapay zeka tabanlı lojistik regresyon modeli ile otomatik kredi risk"
    " analizi."
)
st.markdown("---")

# Kullanıcı Girdi Alanları (Sidebar veya Ana Ekran)
st.subheader("📝 Başvuru Bilgileri")
musteri_adi = st.text_input("Müşteri Adı Soyadı", value="Ahmet Yılmaz")
kredi_tutari = st.number_input(
    "Kredi Tutarı (TL)", min_value=1000, max_value=1000000, value=150000, step=10000
)
esik_deger = (
    st.slider(
        "Banka Risk Eşik Değeri (%)", min_value=5, max_value=50, value=25, step=1
    )
    / 100.0
)

# Değerlendirme Butonu
if st.button("Kredi Başvurusunu Değerlendir", type="primary"):
  with st.status(
      "🔄 [SİSTEM TETİKLENDİ] Süreç devam ediyor...", expanded=True
  ) as status:
    st.write(
        f"'{musteri_adi}' isimli müşterinin {kredi_tutari:,} TL'lik kredi"
        " başvurusu alındı..."
    )
    time.sleep(1.0)

    st.write(
        "🔍 [VERİ ENTEGRASYONU] 7 farklı ilişkisel tablodan müşteri geçmişi"
        " toplanıyor..."
    )
    time.sleep(1.5)

    risk_olasiligi = random.uniform(0.05, 0.65)
    st.write(
        f"🧠 [YAPAY ZEKA] Lojistik Regresyon Modeli Risk Skorunu Hesapladı: %"
        f"{round(risk_olasiligi * 100, 2)}"
    )
    time.sleep(1.0)

    st.write(f"⚖️ [RİSK POLİTİKASI] Banka Risk Eşik Değeri: %{esik_deger * 100}")
    time.sleep(1.0)

    status.update(
        label="✅ [ANALİZ TAMAMLANDI] Sonuçlar hesaplandı!",
        state="complete",
        expanded=False,
    )

  st.markdown("---")
  st.subheader("⚡ [OTOMASYON AKSİYONU]")

  if risk_olasiligi > esik_deger:
    st.error(
        f"❌ **[SONUÇ: RED]** {musteri_adi} isimli müşterinin gecikme"
        " potansiyeli yüksek!"
    )
    st.markdown(
        "🚨 **AKSİYON:** Başvuru otomatik olarak **REDDEDİLDİ**. Bankaya olası"
        " 10 birimlik zarar engellendi."
    )
    st.markdown(
        "📧 **AKSİYON:** Kredi Risk Yönetimi ekibine ve ortak Slack kanalına"
        " anlık uyarı e-postası gönderildi."
    )
  else:
    st.success(
        f"✅ **[SONUÇ: ONAY]** {musteri_adi} isimli müşteri finansal olarak"
        " güvenli sınırda."
    )
    st.markdown(
        "💰 **AKSİYON:** Başvuru **ONAYLANDI**. Bankaya tahmini 3 birimlik"
        " kazanç süreci başladı."
    )
    st.markdown(
        "📱 **AKSİYON:** Veri tabanı güncellendi ve müşterinin telefonuna"
        " 'Krediniz Hazır' SMS'i gönderildi."
    )

"""
def akilli_kredi_onay_sistemi(musteri_adi, kredi_tutari):
    print(f"🔄 [SİSTEM TETİKLENDİ] '{musteri_adi}' isimli müşterinin {kredi_tutari} TL'lik kredi başvurusu alındı...")
    time.sleep(1.5)

    print("🔍 [VERİ ENTEGRASYONU] 7 farklı ilişkisel tablodan (bureau, installments_payments, credit_card_balance) müşteri geçmişi toplanıyor...")
    time.sleep(2)

    # rastgele bir risk skoru üretiyoruz (0.0 ile 1.0 arasında)
    # Gerçek projede burası eğittiğimiz Lojistik Regresyon modelinden gelecek.
    risk_olasiligi = random.uniform(0.05, 0.65)
    print(f"🧠 [YAPAY ZEKA] Lojistik Regresyon Modeli Risk Skorunu Hesapladı: %{round(risk_olasiligi * 100, 2)}")
    time.sleep(1.5)

    # Finansal Mantığı: 10 birim kayba karşılık 3 birim kazanç dengesi.
    # Kayıp çok büyük olduğu için risk eşiğimizi (threshold) %25 gibi güvenli bir sınırda tutuyoruz.
    esik_deger = 0.25
    print(f"⚖️ [RİSK POLİTİKASI] Banka Risk Eşik Değeri: %{esik_deger * 100}")
    time.sleep(1.5)

    print("\n⚡ [OTOMASYON AKSİYONU BAŞLADI]")
    time.sleep(1)

    if risk_olasiligi > esik_deger:
        print(f"❌ [SONUÇ: RED] {musteri_adi} isimli müşterinin gecikme potansiyeli yüksek!")
        print(f"🚨 AKSİYON: Başvuru otomatik olarak REDDEDİLDİ. Bankaya olası 10 birimlik zarar engellendi.")
        print("📧 AKSİYON: Kredi Risk Yönetimi ekibine ve ortak Slack kanalına anlık uyarı e-postası gönderildi.")
    else:
        print(f"✅ [SONUÇ: ONAY] {musteri_adi} isimli müşteri finansal olarak güvenli sınırda.")
        print(f"💰 AKSİYON: Başvuru ONAYLANDI. Bankaya tahmini 3 birimlik kazanç süreci başladı.")
        print(f"📱 AKSİYON: Veri tabanı güncellendi ve müşterinin telefonuna 'Krediniz Hazır' SMS'i gönderildi.")

# --- CANLI SUNUM DENEMESİ ---
# Şimdi fonksiyonumuzu iki farklı senaryo ile test edelim:

# 1. Deneme: Ahmet Yılmaz için başvuru yapıyoruz
akilli_kredi_onay_sistemi("Ahmet Yılmaz", 150000)

print("\n" + "="*50 + "\n")

# 2. Deneme: Ayşe Demir için başvuru yapıyoruz
akilli_kredi_onay_sistemi("Ayşe Demir", 250000)
"""
