def thread_walk(inbox, thread_id):
    """Retrieve full history of a given thread_id sorted by timestamp."""
    thread_msgs = [m for m in inbox if m.get("thread_id") == thread_id]
    return sorted(thread_msgs, key=lambda x: x.get("timestamp", ""))

def find_grounded_context(inbox, target_msg_id):
    msg = next((m for m in inbox if m["id"] == target_msg_id), None)
    if not msg:
        return None, []
        
    thread = thread_walk(inbox, msg.get("thread_id"))
    cited_ids = [m["id"] for m in thread if m["id"] != target_msg_id]
    
    return thread, cited_ids
