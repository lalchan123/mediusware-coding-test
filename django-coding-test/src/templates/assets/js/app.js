import React from "react";
import ReactDOM from "react-dom";
import CreateProduct from "./components/CreateProduct";
import UpdateProduct from "./components/UpdateProduct";

// require('./bootstrap');
// require('./sb-admin');

const propsContainer = document.getElementById("variants");
const props = Object.assign({}, propsContainer.dataset);

console.log("12 id", id);

if (props && id !== 0) {
    ReactDOM.render(
        <React.StrictMode>
            <UpdateProduct props={props} id={id} />
        </React.StrictMode>,
        document.getElementById('root')
    );
} else if (props && id === 0) {
    ReactDOM.render(
        <React.StrictMode>
            <CreateProduct {...props} />
        </React.StrictMode>,
        document.getElementById('root')
    );
}






