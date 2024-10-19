import streamlit as st
import PyPDF2
from openai import OpenAI

# Mostrar título y descripción.
st.title("Manufactura: Caso de uso #4​")
st.subheader("Efectividad de los activos de fábrica.​")
import PyPDF2
from openai import OpenAI

# Mostrar título y descripción.
st.title("Manufactura: Caso de uso #4​")
st.subheader("Efectividad de los activos de fábrica.​")
st.write("📄 Respuestas a preguntas sobre documentos .TX,.MD y .PDF. Sube un documento a continuación y haz una pregunta sobre él – ¡GPT responderá!")
st.write(" Nota: Para usar esta aplicación, necesitas proporcionar una clave de API de OpenAI, que puedes obtener [aquí](https://platform.openai.com/account/api-keys)."
)

# Solicitar al usuario su clave de API de OpenAI mediante `st.text_input`.
# Alternativamente, puedes almacenar la clave de API en `./.streamlit/secrets.toml` y acceder a ella
# mediante `st.secrets`, ver https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("Clave API de OpenAI", type="password")
if not openai_api_key:
    st.info("Por favor, introduce tu clave API para continuar.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # Permitir al usuario cargar un archivo mediante `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Sube un documento (.pdf, .txt o .md)", type=("pdf", "txt", "md")
    )

    # If a file is uploaded
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            # Read and extract text from the PDF
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            document = ""
            for page in range(len(pdf_reader.pages)):
                document += pdf_reader.pages[page].extract_text()

        else:
            # Handle text and markdown files
            document = uploaded_file.read().decode()

        # Ask for a question
        question = st.text_area(
            "Haz una pregunta sobre el documento!",
            placeholder="¿Puedes darme un resumen breve?",
            disabled=not document,
        )

        if question:
            # Prepare the prompt with the document and the question
            messages = [
                {
                    "role": "user",
                    "content": f"Aquí tienes un documento: {document} \n\n---\n\n {question}",
                }
            ]

            # Generate an answer using the OpenAI API
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
            )

            # Display the response
            st.write_stream(stream)