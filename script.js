import { initializeApp } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-app.js";
import { getFirestore, collection, getDocs } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-firestore.js";


let allDevices = [];
let visibleDevices = [];
let selectedBrand = "전체";
let selectedYear = "2026";

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

    const visibleDevices = devices.filter(device => {

        if (!device.model) {
            return false;
        }

        if (device.status === "후보") {
            return false;
        }

        return true;
    });

    visibleDevices.sort((a, b) => {
        return String(a.releaseDate || "").localeCompare(String(b.releaseDate || ""));
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
                <td>${device.releaseDate || "-"}</td>
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

function applyFilters() {
    let filteredDevices = visibleDevices;

    const brandMap = {
        "삼성": "Samsung",
        "애플": "Apple",
        "레노버": "Lenovo"
    };

    if (selectedBrand !== "전체") {
        filteredDevices = filteredDevices.filter(device => {
            return device.brand === brandMap[selectedBrand];
        });
    }

    if (selectedYear !== "전체") {
        filteredDevices = filteredDevices.filter(device => {
            const dateText = device.releaseDate || device.publishedAt || "";
            return String(dateText).includes(selectedYear);
        });
    }

    renderDevices(filteredDevices);
}

window.filterDevices = function (brand) {

    selectedBrand = brand;

    document.querySelectorAll(".brand-btn").forEach(btn => {
        btn.classList.remove("active");
    });

    event.target.classList.add("active");

    applyFilters();
}

window.filterByYear = function (year) {

    selectedYear = year;

    document.querySelectorAll(".year-btn").forEach(btn => {
        btn.classList.remove("active");
    });

    event.target.classList.add("active");

    applyFilters();
}

async function loadDevices() {
    const querySnapshot = await getDocs(collection(db, "devices"));
    
    const devices = []; 

    querySnapshot.forEach((doc) => {
        devices.push(doc.data());
    });

    allDevices = devices;

    visibleDevices = getVisibleDevices(devices);

    const hiddenDevices = devices.filter(d => !visibleDevices.includes(d));

    renderDevices(visibleDevices);
}

loadDevices();