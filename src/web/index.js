import cytoscape from "cytoscape";
import { elements } from "../../build/converted.js";

cytoscape({
    container: document.getElementById("cy"),

    elements: elements,

    layout: {
        name: "breadthfirst",
        // circle: true,
        spacingFactor: 10,
        avoidOverlap: true,
    },

    // so we can see the ids
    style: [
        {
            selector: "node",
            style: {
                label: "data(id)",
            },
        },
    ],
});
