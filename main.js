// const serverIp = `ws://192.168.1.13:8002`; 
// const websocket = new WebSocket(serverIp); // Create WebSocket connection

// websocket.addEventListener("open", () => {
//   console.log("WebSocket connection established.");
// });

// websocket.addEventListener("error", (error) => {
//   console.error("There was an error in the WebSocket Connection:", error);
// });

// websocket.addEventListener("close", () => {
//   console.log("WebSocket connection closed.");
// });


// // if (document.getElementById("messageInput")) {
  
// //   const textInput = document.querySelector("#messageInput");
// //   const fileInput = document.querySelector("#fileInput");
// //   const dateInput = document.querySelector("#dateInput");
// //   const submitButton = document.querySelector(".submitButton");

// //   submitButton.addEventListener("click", async (event) => {
// //     event.preventDefault(); 

// //     const message = textInput.value;
// //     const date = dateInput.value;
// //     const payload = { message, date };

// //     // Check if a file is selected in the file input
// //     const file = fileInput.files[0];
// //     if (file) {
// //       const fileData = await fileToBase64(file);
// //       payload.image = fileData;
// //     }

// //     // Send payload through WebSocket
// //     websocket.send(JSON.stringify(payload));
// //     console.log(payload)
// //     textInput.value = "";
// //     fileInput.value = "";
// //     dateInput.value = "";
// //   });
// // }

// // function to convert file to Base64
// function fileToBase64(file) {
//   return new Promise((resolve, reject) => {
//     const reader = new FileReader();
//     reader.onload = () => resolve(reader.result);
//     reader.onerror = (error) => reject(error);
//     reader.readAsDataURL(file);
//   });
// }

// // Client-side: Receive messages
// websocket.addEventListener("message", ({ data }) => {
//   const notificationArea = document.getElementById("Notification");
//   const imageContainer = document.getElementById("display_image");
//   const messageContainer = document.getElementById("receivedMessage");
//   const dateContainer = document.getElementById("receivedDate");
//   console.log("Received raw data:", data);  // This will print the raw data received

//   const event = JSON.parse(data);
//   console.log("Received event:",event);
//   console.log("help")
//   console.log(event.yolo_class_id)
//   if (event.yolo_class_id !== undefined) {
//     console.log("The YOLO isnt NULL")
//     console.log(event.message)
//     // Display object detection info
//     messageContainer.innerText= `You received a Message ${event.message}`;
//     dateContainer.innerText = `The time of the Frame Is: ${event.frame_time}`;
//     notificationArea.style.display = "block";
//     imageContainer.style.display = "none"; // Modify this to show an image if required
//   } else {
//       // Handle regular messages or fallback response
//       messageContainer.innerHTML = event.message || "No message";
//       dateContainer.innerHTML = "";
//       notificationArea.style.display = "block"; 
//       imageContainer.style.display = "none"; 
//   }

//   // Show notification when the image and message is received
//   // if (event.image) {
//   //   console.log("THE YOLO SENT AN IMAGE")
//   //   imageContainer.src = event.image; 
//   //   imageContainer.style.display = "block";  
//   //   notificationArea.style.display = "none"; 
//   //   messageContainer.innerHTML = event.message || "No message"; 
//   //   dateContainer.innerHTML = `Received on: ${event.date}`; 
//   // } else {
//   //   imageContainer.style.display = "none";  
//   //   notificationArea.style.display = "block"; 
//   //   messageContainer.innerHTML = "No new message"; 
//   //   dateContainer.innerHTML = ""; 
//   // }
// });
const receivedEvents=new Set()
const serverIp = `ws://192.168.1.13:8002`;  
const websocket = new WebSocket(serverIp); // Create WebSocket connection

websocket.addEventListener("open", () => {
  console.log("WebSocket connection established.");
});

websocket.addEventListener("error", (error) => {
  console.error("There was an error in the WebSocket Connection:", error);
});

websocket.addEventListener("close", () => {
  console.log("WebSocket connection closed.");
});

// Ensure the WebSocket connection is open before sending data
function sendMessage(message) {
  if (websocket.readyState === WebSocket.OPEN) {
    websocket.send(JSON.stringify(message));
    console.log("Sent message:", message);
  } else {
    console.error("WebSocket is not open, retrying...");
    setTimeout(() => sendMessage(message), 1000);  // Retry sending after 1 second
  }
}

// Client-side: Receive messages
websocket.addEventListener("message", ({ data }) => {
  const notificationArea = document.getElementById("Notification");
  const imageContainer = document.getElementById("display_image");
  const messageContainer = document.getElementById("receivedMessage");
  const dateContainer = document.getElementById("receivedDate");
  const confidenceContainer = document.getElementById("receivedConfidence")
  //console.log("Received raw data:", data);  // This will print the raw data received

  try {
    
    const event = JSON.parse(data);
    receivedEvents.add(event)
    //console.log("Received event:", event);

    if (event.yolo_class_id !== undefined) {
      // console.log("YOLO class detected");
      confidenceContainer.innerText=`The confidence of the Model is : ${event.confidence}`
      messageContainer.innerText = `You received a Message: ${event.message}`;
      dateContainer.innerText = `The time of the Frame Is: ${event.frame_time}`;
      notificationArea.style.display = "block";
      imageContainer.style.display = "none";  // Modify this to show an image if required
    } else {
      // Handle regular messages or fallback response
      messageContainer.innerHTML = event.message || "No message";
      dateContainer.innerHTML = "";
      notificationArea.style.display = "block";
      imageContainer.style.display = "none";
    }
    if (event.frame_image) {
      //console.log("THE YOLO SENT AN IMAGE")
      const base64Image = `data:image/jpg;base64,${event.frame_image}`;

      imageContainer.src = base64Image; 
      imageContainer.style.display = "block";  
      notificationArea.style.display = "none"; 
    } else {
      imageContainer.style.display = "none";  
      notificationArea.style.display = "block"; 
    }
  } catch (e) {
    console.error("Error parsing message:", e);
  }
  console.log(Array.from(receivedEvents))
});


