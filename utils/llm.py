import ollama

class LLMClient:
    def __init__(self, model_name="gemma3:1b"):
        self.model_name = model_name

    def generate_response(self, prompt, context=None, system_prompt=None):
        """
        Generates a response from the Ollama model.
        
        Args:
            prompt (str): The user's input.
            context (str, optional): Retrieved context from RAG.
            system_prompt (str, optional): System instructions.
        
        Returns:
            str: The model's response.
        """
        try:
            messages = []
            if system_prompt:
                messages.append({'role': 'system', 'content': system_prompt})
            
            full_prompt = prompt
            if context:
                full_prompt = f"Context:\n{context}\n\nUser Question:\n{prompt}"
            
            messages.append({'role': 'user', 'content': full_prompt})

            response = ollama.chat(model=self.model_name, messages=messages)
            return response['message']['content']
        except Exception as e:
            return f"Error communicating with Ollama: {str(e)}"

    def list_models(self):
        try:
            models = ollama.list()
            return [m['name'] for m in models['models']]
        except:
            return []
