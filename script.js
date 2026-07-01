import { initializeApp } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-app.js";
import { getFirestore, collection, getDocs } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-firestore.js";


let allDevices = [];
let visibleDevices = [];

const firebaseConfig = {
    apiKey: "AIzaSyAvpfJGYP5wmuhIsW2dFxO7Cu1fUZOsCjw",
    authDomain: "seat-picker-fdea4.firebaseapp.com",
    projectId: "seat-picker-fdea4",
    storageBucket: "seat-picker-fdea4.firebasestorage.app",
    messagingSenderId: "366627890858",
    appId: "1:366627890858:web:a19f63ca2225afbc88d2d3"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

const tableBody = document.getElementById("deviceTableBody");

function getStatus(releaseDate) {

    const today = new Date();

    const release = new Date(releaseDate);

    if (release > today) {
        return "출시 예정";
    }

    return "출시 완료";
}

const today = new Date();

const oneYearAgo = new Date(today);
oneYearAgo.setFullYear(today.getFullYear() - 1);

const oneYearLater = new Date(today);
oneYearLater.setFullYear(today.getFullYear() + 1);

function getVisibleDevices(devices) {
    const today = new Date();

    const oneYearAgo = new Date(today);
    oneYearAgo.setFullYear(today.getFullYear() - 1);

    const oneYearLater = new Date(today);
    oneYearLater.setFullYear(today.getFullYear() + 1);

    const visibleDevices = devices.filter(device => {

    if (!device.model) {
        return false;
    }

    if (device.status === "후보") {
        return false;
    }

    if (!device.releaseDate) {
        return true;
    }

    const releaseDate = new Date(device.releaseDate);

    return releaseDate >= oneYearAgo &&
           releaseDate <= oneYearLater;
    });

    visibleDevices.sort((a, b) => {
        return new Date(a.releaseDate) - new Date(b.releaseDate);
    });

    return visibleDevices;
}

function renderDevices(deviceList) {

    tableBody.innerHTML = "";

    deviceList.forEach((device, index) => {

        const row = `
            <tr>
                <td>${index + 1}</td>
                <td>${device.brand}</td>
                <td>${device.type}</td>
                <td>${device.model}</td>
                <td class="${getStatus(device.releaseDate) === '출시 완료' ? 'released' : 'upcoming'}">
                 ${getStatus(device.releaseDate)}
                </td>
                <td>${device.releaseDate}</td>
                <td>
                 ${
                     device.link
                    ? `<a href="${device.link}" target="_blank">보기</a>`
                     : "-"
                }
                </td>
            </tr>
        `;

        tableBody.innerHTML += row;
    });
}

window.filterDevices = function (brand) {

    if (brand === "전체") {
        renderDevices(visibleDevices);
        return;
    }

    const brandMap = {
        "삼성": "Samsung",
        "애플": "Apple",
        "레노버": "Lenovo"
    };

    const filteredDevices = visibleDevices.filter(device => {
        return device.brand === brandMap[brand];
    });

    renderDevices(filteredDevices);
}

async function loadDevices() {
    const querySnapshot = await getDocs(collection(db, "devices"));
    
    const devices = []; 

    querySnapshot.forEach((doc) => {
        devices.push(doc.data());
    });

    allDevices = devices;

    visibleDevices = getVisibleDevices(devices);

    renderDevices(visibleDevices);
}

loadDevices();