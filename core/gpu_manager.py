"""CreatorClip Factory - GPU Resource Scheduler & Monitor
Manages sequential execution, VRAM thresholds, and safe fallback for RTX 4050 (6GB).
"""
import subprocess
import threading
import time
from typing import Dict, Any, Tuple

class GPUResourceManager:
    _lock = threading.Lock()
    _active_task: str = "idle"

    @classmethod
    def get_gpu_status(cls) -> Dict[str, Any]:
        """Queries nvidia-smi for VRAM utilization, temperature, and power."""
        try:
            cmd = [
                "nvidia-smi",
                "--query-gpu=name,memory.total,memory.used,memory.free,temperature.gpu,utilization.gpu",
                "--format=csv,noheader,nounits"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=5)
            lines = res.stdout.strip().split("\n")
            if lines and lines[0]:
                parts = [p.strip() for p in lines[0].split(",")]
                name = parts[0]
                total_mb = float(parts[1])
                used_mb = float(parts[2])
                free_mb = float(parts[3])
                temp_c = float(parts[4])
                util_pct = float(parts[5])
                return {
                    "available": True,
                    "name": name,
                    "total_mb": total_mb,
                    "used_mb": used_mb,
                    "free_mb": free_mb,
                    "temp_c": temp_c,
                    "util_pct": util_pct,
                    "current_task": cls._active_task
                }
        except Exception as e:
            return {
                "available": False,
                "error": str(e),
                "total_mb": 6144,
                "used_mb": 0,
                "free_mb": 6144,
                "current_task": cls._active_task
            }

    @classmethod
    def can_run_gpu_task(cls, required_vram_mb: float = 1500) -> Tuple[bool, str]:
        status = cls.get_gpu_status()
        if not status["available"]:
            return False, "GPU unavailable (nvidia-smi failed), CPU fallback required"
        
        # Keep a safety reserve of at least 800 MB VRAM
        if status["free_mb"] < (required_vram_mb + 800):
            return False, f"Insufficient free VRAM ({status['free_mb']:.1f} MB free, need {required_vram_mb + 800:.1f} MB)"
        
        return True, "GPU ready"

    @classmethod
    def acquire_execution_lock(cls, task_name: str, timeout_sec: float = 60.0) -> bool:
        """Acquires lock for sequential execution of heavy tasks (Ollama, Real-ESRGAN, Heavy Render)."""
        start = time.time()
        while time.time() - start < timeout_sec:
            if cls._lock.acquire(blocking=False):
                cls._active_task = task_name
                return True
            time.sleep(0.5)
        return False

    @classmethod
    def release_execution_lock(cls):
        cls._active_task = "idle"
        try:
            cls._lock.release()
        except RuntimeError:
            pass

    @classmethod
    def get_optimal_upscale_tile_size(cls) -> int:
        """Returns safe tile size for Real-ESRGAN on 6GB VRAM."""
        status = cls.get_gpu_status()
        free = status.get("free_mb", 3000)
        if free > 4000:
            return 400
        elif free > 2500:
            return 256
        else:
            return 128

if __name__ == "__main__":
    status = GPUResourceManager.get_gpu_status()
    print("GPU Status:", status)
    ok, msg = GPUResourceManager.can_run_gpu_task(1000)
    print("Can run 1000MB task:", ok, msg)
    print("Optimal upscale tile size:", GPUResourceManager.get_optimal_upscale_tile_size())
