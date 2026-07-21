const dialogue = [

    {"interval": 0.1, "dialogue": "ikaw kasi ehh....", "delay": 0.9},
    {"interval": 0.5, "dialogue": "", "delay": 0.2},
    {"interval": 1.5, "dialogue": "close na kayooo", "delay": 0.4},
    {"interval": 2.1, "dialogue": "naggg ", "delay": 0.1},
    {"interval": 0.1, "dialogue": "confessss", "delay": 0.2},
    {"interval": 0, "dialogue": "Kaaaa paaaa", "delay": 0.2},
]

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms * 1000));
}

function display_wolf(number) {
    let wolf = document.getElementById("wolf");
    if (wolf) {
        wolf.remove();
    }
    wolf = document.createElement("img");
    wolf.src = `${number}.jpg`;
    wolf.alt = "wolf";
    wolf.id = "wolf";
    document.body.appendChild(wolf);
}

async function display(message, delay) {
    let message_element = document.getElementById("message");
    message_element.innerHTML = "";
    const list_messages = message.split("");
    for (msg in list_messages) {
        let word_delay = delay / list_messages.length;
        message_element.innerHTML += list_messages[msg];
        await sleep(word_delay);
    }
}

async function OrangeANDLemons() {
    for (item in dialogue) {
        if (Number(item) === 2) {
            display_wolf(0);
        }
        else if(Number(item) === 3) {
            display_wolf(1);
        }
        await display(dialogue[item]["dialogue"], dialogue[item]["delay"]);
        await sleep(dialogue[item]["interval"]);
    }
}

OrangeANDLemons();