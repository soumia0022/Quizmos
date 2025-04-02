import {renderChoice} from "../../static/js/lecturer_poll_display/questions/choice_display";

test("renderChoice should generate correct HTML for a question", () => {
    const question = {
        id: 1,
        text: "What is your favorite color?",
        options: ["Red", "Blue", "Green"]
    };

    const html = renderChoice(question);

    // Load the HTML into JSDOM
    document.body.innerHTML = html;

    // Verify question text
    expect(document.querySelector("p").textContent).toBe("What is your favorite color?");

    // Verify options
    const options = document.querySelectorAll(".response-card label");
    expect(options).toHaveLength(3);
    expect(options[0].textContent).toBe("Red");
    expect(options[1].textContent).toBe("Blue");
    expect(options[2].textContent).toBe("Green");

    // Verify progress bars
    const progressBars = document.querySelectorAll(".progress-bar");
    expect(progressBars).toHaveLength(3);
    expect(progressBars[0].style.width).toBe("0%");
});
