while true; do
    python main.py --agent_type dynamic
    echo "Script crashed with exit code $? at $(date)" >> crash_test_llama_dynpol.log
    sleep 5
done

