#!/bin/bash

# Function to kill background processes on exit
cleanup() {
    echo "Stopping servers..."
    kill $BACKEND_PID $STREAMLIT_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM EXIT

# Start FastAPI in the background
echo "Starting FastAPI backend on port 8000..."
python3 app.py > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to be ready
echo "Waiting for backend to start..."
MAX_RETRIES=10
COUNT=0
while ! curl -s http://localhost:8000/status > /dev/null; do
    sleep 1
    COUNT=$((COUNT+1))
    if [ $COUNT -ge $MAX_RETRIES ]; then
        echo "Backend failed to start. Check backend.log"
        exit 1
    fi
done
echo "Backend is up!"

# Start Streamlit
echo "Starting Streamlit frontend on port 8501..."
streamlit run streamlit_app.py --server.port 8501 &
STREAMLIT_PID=$!

echo "--------------------------------------------------"
echo "DDR Report Generator is running!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:8501"
echo "--------------------------------------------------"

# Keep script running to maintain background processes
wait
