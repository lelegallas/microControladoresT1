#!/usr/bin/env python3
# Lê umidade (A0) e luz (A1) do ADS1115 e imprime em JSON para o Node-RED.
# Os valores são convertidos para a mesma escala do Pico (0 a 65535),
# então o limite de 60000 continua valendo.

import json
import time

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

ENDERECO = 0x48      # ADDR ligado no GND
VREF_PICO = 3.3      # tensão máxima dos sensores
FAIXA_ADS = 4.096    # ganho ±4,096 V


def ler_canal(bus, canal):
    # Leitura única: OS=1, entrada AINx vs GND, ±4,096 V, 128 SPS, comparador desligado
    config = 0x8000 | ((4 + canal) << 12) | (1 << 9) | (1 << 8) | (4 << 5) | 0x03
    bus.write_i2c_block_data(ENDERECO, 0x01, [config >> 8, config & 0xFF])
    time.sleep(0.01)
    dados = bus.read_i2c_block_data(ENDERECO, 0x00, 2)
    bruto = (dados[0] << 8) | dados[1]
    if bruto > 32767:
        bruto -= 65536
    tensao = bruto * FAIXA_ADS / 32768
    valor = int(tensao / VREF_PICO * 65535)
    return max(0, min(65535, valor))


try:
    with SMBus(1) as bus:
        print(json.dumps({
            "umidade": ler_canal(bus, 0),
            "luz": ler_canal(bus, 1)
        }))
except Exception as e:
    print(json.dumps({"erro": str(e)}))
