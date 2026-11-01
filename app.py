import base64
import hmac
import random
import time
from email.message import EmailMessage

import streamlit as st
from google.auth.exceptions import GoogleAuthError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


st.set_page_config(
    page_title="Akıllı Kredi Onay Sistemi",
    page_icon="💳",
    layout="centered",
)


def eposta_gonder(sonuc):
    ayarlar = st.secrets["gmail"]

    credentials = Credentials(
        token=None,
        refresh_token=ayarlar["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=ayarlar["client_id"],
        client_secret=ayarlar["client_secret"],
    )

    mesaj = EmailMessage()
    mesaj["To"] = ayarlar["recipient"]
    mesaj["Subject"] = "Demo: Kredi değerlendirme sonucu"
    mesaj.set_content(
        f"Müşteri: {sonuc['ad']}\n"
        f"Kredi tutarı: {sonuc['tutar']:,} TL\n"
        f"Risk olasılığı: %{sonuc['risk'] * 100:.2f}\n"
        f"Risk eşiği: %{sonuc['esik'] * 100:.0f}\n"
        f"Sonuç: {sonuc['karar']}\n\n"
        "Bu bir demodur. Risk skoru rastgele üretilmiştir; "
        "gerçek kredi değerlendirmesi değildir."
    )

    ham_mesaj = base64.urlsafe_b64encode(
        mesaj.as_bytes()
    ).decode("ascii")

    with build(
        "gmail", "v1",
        credentials=credentials,
        cache_discovery=False,
    ) as servis:
        servis.users().messages().send(
            userId="me",
            body={"raw": ham_mesaj},
        ).execute(num_retries=0)


st.title("💳 Akıllı Kredi Onay Sistemi")
st.caption(
    "Demo: Risk skoru rastgele üretilir. "
    "Gerçek model, veri tabanı veya SMS bağlantısı yoktur."
)
st.divider()

st.subheader("📝 Başvuru Bilgileri")

musteri_adi = st.text_input(
    "Müşteri Adı Soyadı",
    value="Ahmet Yılmaz",
)
kredi_tutari = st.number_input(
    "Kredi Tutarı (TL)",
    min_value=1000,
    max_value=1000000,
    value=150000,
    step=10000,
)
esik_deger = st.slider(
    "Banka Risk Eşik Değeri (%)",
    min_value=5,
    max_value=50,
    value=25,
) / 100

if st.button("Kredi Başvurusunu Değerlendir", type="primary"):
    if not musteri_adi.strip():
        st.warning("Lütfen müşteri adını gir.")
    else:
        with st.status("Değerlendiriliyor...", expanded=True) as status:
            st.write("Demo başvurusu alındı.")
            time.sleep(1)

            risk = random.uniform(0.05, 0.65)
            st.write(f"Demo risk skoru: %{risk * 100:.2f}")

            st.session_state["sonuc"] = {
                "ad": musteri_adi.strip(),
                "tutar": kredi_tutari,
                "risk": risk,
                "esik": esik_deger,
                "karar": "RED" if risk > esik_deger else "ONAY",
            }
            st.session_state["mail_gonderildi"] = False
            status.update(
                label="Değerlendirme tamamlandı!",
                state="complete",
                expanded=False,
            )

if "sonuc" in st.session_state:
    sonuc = st.session_state["sonuc"]
    st.divider()
    st.subheader("Değerlendirme Sonucu")

    metin = (
        f"{sonuc['ad']} — {sonuc['tutar']:,} TL\n\n"
        f"Risk: %{sonuc['risk'] * 100:.2f} | "
        f"Eşik: %{sonuc['esik'] * 100:.0f}\n\n"
        f"Demo kararı: **{sonuc['karar']}**"
    )

    if sonuc["karar"] == "RED":
        st.error(metin)
    else:
        st.success(metin)

    st.caption(
        "E-posta yalnızca ayarlarda belirlenen deneme adresine gönderilir."
    )

    with st.form("eposta_formu", clear_on_submit=True):
        parola = st.text_input("Gönderim parolası", type="password")
        gonder = st.form_submit_button(
            "📧 Sonucu e-postayla gönder",
            disabled=st.session_state.get("mail_gonderildi", False),
        )

    if gonder:
        ayarlar = st.secrets["gmail"]
        parola_dogru = hmac.compare_digest(
            parola.encode("utf-8"),
            ayarlar["send_password"].encode("utf-8"),
        )

        if not parola_dogru:
            st.error("Gönderim parolası yanlış.")
        else:
            try:
                with st.spinner("E-posta gönderiliyor..."):
                    eposta_gonder(sonuc)
                st.session_state["mail_gonderildi"] = True
                st.rerun()
            except GoogleAuthError:
                st.error(
                    "Gmail yetkilendirmesi başarısız. "
                    "Client bilgilerini ve refresh token'ı kontrol et."
                )
            except HttpError as hata:
                st.error(
                    f"Gmail gönderimi başarısız. HTTP kodu: "
                    f"{hata.resp.status}"
                )
            except Exception:
                st.error(
                    "Gönderim tamamlanamadı. "
                    "Secrets ayarlarını ve uygulama loglarını kontrol et."
                )

    if st.session_state.get("mail_gonderildi", False):
        st.success("E-posta Gmail tarafından gönderim için kabul edildi ✅")
