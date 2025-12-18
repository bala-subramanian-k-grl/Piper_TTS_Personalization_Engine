import argparse
import json
import subprocess
import time
from pathlib import Path

from logger import get_logger
from profile_builder import build_profile

log = get_logger(__name__)

PIPER_EXE = r"C:\piper\piper\piper"
MODEL = r"C:\piper\piper\en_US-kathleen-low.onnx"


def synth_with_profile(text: str, profile_path: str, out_path: str):
    profile = json.loads(Path(profile_path).read_text(encoding="utf-8"))
    params = profile["piper_runtime_params"]

    cmd = (
        f'"{PIPER_EXE}" '
        f'--model "{MODEL}" '
        f'--length_scale {params["length_scale"]} '
        f'--noise_scale {params["noise_scale"]} '
        f'--noise_w {params["noise_w"]} '
        f'--output_file "{out_path}"'
    )

    log.info(
        f"Preparing Piper synthesis: profile={profile_path}, "
        f"params={params}, text_len={len(text)}, output={out_path}"
    )
    log.info(f"Piper command: {cmd}")

    start = time.perf_counter()
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True,  # Windows: run command string via shell
    )
    stdout, stderr = proc.communicate(text)
    elapsed = time.perf_counter() - start

    log.info(f"Piper stdout: {stdout.strip()}")
    log.info(f"Piper stderr: {stderr.strip()}")
    log.info(f"Piper synthesis finished in {elapsed:.3f}s with returncode={proc.returncode}")

    if proc.returncode != 0:
        # This will also be picked up by the outer try/except and logged
        raise RuntimeError(f"Piper failed with code {proc.returncode}")


def main():
    parser = argparse.ArgumentParser(
    description="Piper personalization engine CLI (Windows)")
    parser.add_argument(
    "--train-profile",
    action="store_true",
    help="Analyze user_clean.wav and build voice_profile.json",)
    parser.add_argument(
    "--profile",
    type=str,
    default="voice_profile.json",
    help="Path to profile JSON",)
    parser.add_argument(
    "--text",
    type=str,
    help="Text to synthesize",)
    parser.add_argument(
    "--output",
    type=str,
    default="personalized.wav",
    help="Output WAV file",)
    parser.add_argument(
    "--compare",
    action="store_true",
    help="Generate both baseline and personalized audio for comparison",)

    args = parser.parse_args()



    if args.train_profile:
        log.info("Starting profile training from user_clean.wav")
        profile = build_profile()
        log.info("Profile saved to voice_profile.json")
        print(json.dumps(profile, indent=2))
        # If compare mode is requested, generate baseline + personalized audio
    if args.compare and args.text:
        # 1) Baseline Piper output (no personalization parameters)
        baseline_out = "baseline_compare.wav"
        cmd_base = (
            f'"{PIPER_EXE}" '
            f'--model "{MODEL}" '
            f'--output_file "{baseline_out}"'
        )
        log.info(f"Baseline Piper command: {cmd_base}")
        start = time.perf_counter()
        proc = subprocess.Popen(
            cmd_base,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )
        stdout, stderr = proc.communicate(args.text)
        elapsed = time.perf_counter() - start
        log.info(f"Baseline Piper finished in {elapsed:.3f}s rc={proc.returncode}")
        log.info(f"Baseline stdout: {stdout.strip()}")
        log.info(f"Baseline stderr: {stderr.strip()}")

        # 2) Personalized output (uses your existing synth_with_profile)
        synth_with_profile(args.text, args.profile, args.output)

        print(f"Baseline: {baseline_out}")
        print(f"Personalized: {args.output}")
        return


    if args.text:
        log.info(f"Starting personalized synthesis using profile={args.profile}")
        synth_with_profile(args.text, args.profile, args.output)
        log.info(f"Saved synthesized audio to {args.output}")
        print(f"Saved synthesized audio to {args.output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        
        log.exception(f"Unhandled exception: {e}")
        raise
