import threading
import time
import os
from enum import Enum

class LuzSemaforo(Enum):
    VERMELHO = 0
    AMARELO = 1
    VERDE = 2

class Semaforo:
    def __init__(self):
        self.lock = threading.Lock()
        self.luz_atual = LuzSemaforo.VERMELHO
        self.estado_alterado = threading.Event()
        self.executando = True

    def mudar_luz(self, luz, duracao):
        with self.lock:
            self.luz_atual = luz
            self.estado_alterado.set()  # Notifica que o estado mudou
            
        time.sleep(duracao)  # Mantém esta luz ativa pelo tempo especificado

    def ciclo_semaforo(self):
        while self.executando:
            # Ciclo completo do semáforo
            self.mudar_luz(LuzSemaforo.VERMELHO, 5)
            if not self.executando:
                break
                
            self.mudar_luz(LuzSemaforo.AMARELO, 2)
            if not self.executando:
                break
                
            self.mudar_luz(LuzSemaforo.VERDE, 5)
            if not self.executando:
                break

    def exibir_estado(self):
        ultimo_estado = None
        while self.executando:
            with self.lock:
                estado_atual = self.luz_atual
                
            if estado_atual != ultimo_estado:
                self.limpar_tela()
                print("\n\n")
                
                # Exibe o semáforo com a luz atual ativa
                print(f"{'🔴' if estado_atual == LuzSemaforo.VERMELHO else '⚫'} VERMELHO")
                print(f"{'🟡' if estado_atual == LuzSemaforo.AMARELO else '⚫'} AMARELO")
                print(f"{'🟢' if estado_atual == LuzSemaforo.VERDE else '⚫'} VERDE")
                
                # Mensagem baseada na luz atual
                if estado_atual == LuzSemaforo.VERMELHO:
                    print("\nPare! Sinal vermelho.")
                elif estado_atual == LuzSemaforo.AMARELO:
                    print("\nAtenção! Sinal vai mudar.")
                else:
                    print("\nSiga em frente! Sinal verde.")
                    
                ultimo_estado = estado_atual
                
            # Espera pela notificação de mudança de estado ou verifica a cada 0.5 segundos
            self.estado_alterado.wait(0.5)
            self.estado_alterado.clear()
    
    def contar_tempo(self):
        while self.executando:
            with self.lock:
                estado_atual = self.luz_atual
                
            # Define o tempo baseado na luz atual
            if estado_atual == LuzSemaforo.VERMELHO or estado_atual == LuzSemaforo.VERDE:
                tempo_total = 5
            else:
                tempo_total = 2
                
            # Contagem regressiva
            for i in range(tempo_total, 0, -1):
                with self.lock:
                    # Verifica se o estado mudou durante a contagem
                    if estado_atual != self.luz_atual:
                        break
                        
                print(f"Tempo restante: {i} segundos", end="\r")
                time.sleep(1)
            
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def parar(self):
        self.executando = False
        self.estado_alterado.set()  # Garante que as threads não fiquem bloqueadas

def main():
    try:
        semaforo = Semaforo()
        
        # Cria threads para cada função do semáforo
        thread_ciclo = threading.Thread(target=semaforo.ciclo_semaforo)
        thread_exibicao = threading.Thread(target=semaforo.exibir_estado)
        thread_contador = threading.Thread(target=semaforo.contar_tempo)
        
        # Define as threads como daemon para que encerrem quando o programa principal encerrar
        thread_ciclo.daemon = True
        thread_exibicao.daemon = True
        thread_contador.daemon = True
        
        print("Simulação de Semáforo com Threads")
        print("Pressione Ctrl+C para encerrar o programa.")
        time.sleep(2)
        
        # Inicia as threads
        thread_ciclo.start()
        thread_exibicao.start()
        thread_contador.start()
        
        # Mantém o programa principal rodando
        while True:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        if 'semaforo' in locals():
            semaforo.parar()  # Sinaliza para as threads pararem
        print("\nPrograma encerrado pelo usuário.")

if __name__ == "__main__":
    main()