import gradio as gr
from generate import answer

def handle_query(question):
    if not question.strip():
        return "", ""
    result = answer(question)
    return result["answer"], result["sources"]

with gr.Blocks(title="Drexel PHC Unofficial Guide") as demo:
    gr.Markdown("## Drexel Panhellenic Unofficial Recruitment Guide")
    gr.Markdown("Ask anything about sorority recruitment at Drexel. Answers come from GreekRank, Reddit, and official Drexel PHC sources only.")

    inp = gr.Textbox(label="Your question", placeholder="e.g. What is it like to rush Delta Zeta?")
    btn = gr.Button("Ask")
    answer_box = gr.Textbox(label="Answer", lines=8)
    sources_box = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer_box, sources_box])
    inp.submit(handle_query, inputs=inp, outputs=[answer_box, sources_box])

demo.launch()
