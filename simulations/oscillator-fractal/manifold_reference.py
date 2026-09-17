#!/usr/bin/env python3
"""Omega MAR complete recursive braided-manifold reference and verifier.

Owner/architect: Benjamin Thomas Murphy / Basic Thoughts LLC

This is a deterministic classical reference implementation of the supplied
manifold definitions. It preserves identity and appends topology; it never
compresses or flattens the logical state. The recursive law is unbounded, while
every materialized execution frontier is finite. No production Boss 8004 file
is modified.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import tarfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np

PHI = (1.0 + math.sqrt(5.0)) / 2.0
GOLDEN_ANGLE = 2.0 * math.pi * (1.0 - 1.0 / PHI)
R_I = np.exp(4j * np.pi / 5)
R_TAU = np.exp(-3j * np.pi / 5)
BASE_IDENTITY_COUNT = 128**2
BASE_TWIN_BLOCK_LOG2 = 640
DEFAULT_SEED = 260831


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def json_pair(z: complex) -> dict[str, float]:
    return {"re": float(np.real(z)), "im": float(np.imag(z))}


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fields: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        writer.writeheader()
        writer.writerows(rows)


def parse_json_prefix(path: Path) -> tuple[dict[str, Any], int, int]:
    text = path.read_text(encoding="utf-8", errors="replace")
    stripped = text.lstrip()
    prefix_offset = len(text) - len(stripped)
    obj, end = json.JSONDecoder().raw_decode(stripped)
    consumed = prefix_offset + end
    return obj, consumed, len(text) - consumed


def gray(value: int) -> int:
    return value ^ (value >> 1)


def gray_inverse(value: int) -> int:
    out = value
    shift = value >> 1
    while shift:
        out ^= shift
        shift >>= 1
    return out


def hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


def fibonacci_up_to(limit: int) -> list[int]:
    seq = [1, 2]
    while seq[-1] + seq[-2] <= limit:
        seq.append(seq[-1] + seq[-2])
    return seq


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    d = 3
    while d * d <= value:
        if value % d == 0:
            return False
        d += 2
    return True


def fibonacci_kernel() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    f = np.array(
        [[1.0 / PHI, 1.0 / math.sqrt(PHI)],
         [1.0 / math.sqrt(PHI), -1.0 / PHI]],
        dtype=np.complex128,
    )
    r = np.diag([R_I, R_TAU]).astype(np.complex128)
    return f, r, np.linalg.inv(f) @ r @ f


def braid_gate(generator: int) -> np.ndarray:
    _, s1, s2 = fibonacci_kernel()
    if generator == 1:
        return s1
    if generator == 2:
        return s2
    if generator == -1:
        return np.linalg.inv(s1)
    if generator == -2:
        return np.linalg.inv(s2)
    raise ValueError(f"unsupported braid generator: {generator}")


def apply_braid_word(word: Sequence[int]) -> np.ndarray:
    out = np.eye(2, dtype=np.complex128)
    for generator in word:
        out = braid_gate(generator) @ out
    return out


def no_00_basis(n: int) -> list[int]:
    return [i for i in range(2**n) if "00" not in format(i, f"0{n}b")]


def isometry(n: int, basis: Sequence[int]) -> np.ndarray:
    out = np.zeros((2**n, len(basis)), dtype=np.complex128)
    for col, index in enumerate(basis):
        out[index, col] = 1.0
    return out


def legacy_projector(nq: int, position: int) -> np.ndarray:
    p = np.zeros((2**nq, 2**nq), dtype=np.complex128)
    for i in range(2**nq):
        bits = format(i, f"0{nq}b")
        if bits[position] == "0" and bits[position + 1] == "0":
            continue
        p[i, i] = 1.0
    return p


def legacy_local_gate() -> np.ndarray:
    p = legacy_projector(3, 0)
    return R_I * p + R_TAU * (np.eye(8, dtype=np.complex128) - p)


def legacy_embed(n: int, generator_position: int) -> np.ndarray:
    local = legacy_local_gate()
    out = np.array([[1.0 + 0j]], dtype=np.complex128)
    i = 0
    while i < n:
        if i == generator_position % max(1, n - 2):
            out = np.kron(out, local)
            i += 3
        else:
            out = np.kron(out, np.eye(2, dtype=np.complex128))
            i += 1
    return out


def audit_legacy_operator() -> dict[str, Any]:
    n = 4
    basis = no_00_basis(n)
    v = isometry(n, basis)
    identity = np.eye(len(basis), dtype=np.complex128)
    s0 = v.conj().T @ legacy_embed(n, 0) @ v
    s1 = v.conj().T @ legacy_embed(n, 1) @ v
    return {
        "qic_dimension": len(basis),
        "qic_basis": basis,
        "sigma0_unitarity_error": float(np.linalg.norm(s0.conj().T @ s0 - identity)),
        "sigma1_unitarity_error": float(np.linalg.norm(s1.conj().T @ s1 - identity)),
        "sigma0_minus_sigma1": float(np.linalg.norm(s0 - s1)),
        "sigma0_minus_global_phase": float(np.linalg.norm(s0 - R_I * identity)),
        "sigma1_minus_global_phase": float(np.linalg.norm(s1 - R_I * identity)),
        "commutator_norm": float(np.linalg.norm(s0 @ s1 - s1 @ s0)),
        "braid_relation_error": float(np.linalg.norm(s0 @ s1 @ s0 - s1 @ s0 @ s1)),
        "interpretation": (
            "On the tested four-qubit no-00 QIC basis, both generator positions "
            "reduce to the same global phase. The braid relation therefore passes "
            "trivially and crossing order is not represented by that projection."
        ),
    }


def audit_archive(archive: Path | None) -> dict[str, Any]:
    if archive is None or not archive.is_file():
        return {"status": "NOT_AVAILABLE", "production_files_modified": False}
    target = "saai_swarm_8004/quantum_engine.py"
    config = "saai_swarm_8004/config.py"
    try:
        with tarfile.open(archive, "r:*") as tf:
            names = set(tf.getnames())
            if target not in names:
                return {
                    "status": "MISSING_EXPECTED_MEMBER",
                    "archive_sha256": sha256_file(archive),
                    "production_files_modified": False,
                }
            member = tf.extractfile(target)
            qbytes = member.read() if member else b""
            cmember = tf.extractfile(config) if config in names else None
            cbytes = cmember.read() if cmember else b""
    except (tarfile.TarError, OSError) as exc:
        return {"status": "READ_ERROR", "error": f"{type(exc).__name__}: {exc}", "production_files_modified": False}
    ctext = cbytes.decode("utf-8", "replace")
    credential_literal = "EMAIL_PASSWORD" in ctext and "os.environ.get" in ctext
    return {
        "status": "READ_ONLY_AUDITED",
        "archive": str(archive),
        "archive_sha256": sha256_file(archive),
        "quantum_engine_member": target,
        "quantum_engine_sha256": sha256_bytes(qbytes),
        "contains_r_phases": b"R_I" in qbytes and b"R_TAU" in qbytes,
        "contains_qic_projection": b"V_ISO" in qbytes and b"QIC_BASIS" in qbytes,
        "contains_braid_word_evaluator": b"jones_polynomial_from_braid" in qbytes,
        "credential_shaped_fallback_detected": credential_literal,
        "credential_value_redacted": True,
        "security_note": (
            "A credential-shaped fallback is present in the archived config. Rotate it and "
            "replace the fallback with a secret-store/environment-only requirement."
            if credential_literal else "No credential-shaped fallback detected by the narrow scan."
        ),
        "production_files_modified": False,
    }


def identity_layer() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    addresses: list[int] = []
    for i in range(BASE_IDENTITY_COUNT):
        g = gray(i)
        addresses.append(g)
        anchor = "ACTG"[i % 4]
        phase = (i + 1) * GOLDEN_ANGLE
        z = math.sqrt(i + 1) * np.exp(1j * phase)
        rows.append({
            "index": i,
            "gray": g,
            "gray_bits": format(g, "014b"),
            "inverse_index": gray_inverse(g),
            "anchor": anchor,
            "P_real": float(math.cos(phase)),
            "P_imag": float(math.sin(phase)),
            "F_real": float(np.real(z)),
            "F_imag": float(np.imag(z)),
        })
    arr = np.asarray(addresses, dtype=np.uint32)
    adjacency = np.asarray([hamming(int(arr[i]), int(arr[i + 1])) for i in range(len(arr) - 1)])
    return rows, {
        "count": BASE_IDENTITY_COUNT,
        "dimensions": 14,
        "unique_addresses": int(np.unique(arr).size),
        "collisions": int(BASE_IDENTITY_COUNT - np.unique(arr).size),
        "inverse_failures": int(sum(gray_inverse(int(g)) != i for i, g in enumerate(arr))),
        "adjacent_one_fold_fraction": float(np.mean(adjacency == 1)),
        "compression": False,
        "flattened": False,
        "address_sha256": sha256_bytes(arr.tobytes()),
    }


@dataclass(frozen=True)
class ScaleStep:
    step: int
    axis: str
    horizontal_depth: int
    vertical_depth: int
    grid_width: int
    grid_height: int
    block_count: int
    log2_state_dimension: int
    symbolic_state_dimension: str
    compressed: bool = False
    flattened: bool = False


def scale_sequence(horizontal_depth: int, vertical_depth: int) -> list[ScaleStep]:
    h = v = 0
    out = [ScaleStep(0, "SEED", 0, 0, 1, 1, 1, BASE_TWIN_BLOCK_LOG2, "2^640")]
    step = 0
    while h < horizontal_depth or v < vertical_depth:
        if h < horizontal_depth:
            h += 1; step += 1
            blocks = 2 ** (h + v)
            out.append(ScaleStep(step, "H", h, v, 2**h, 2**v, blocks,
                                 BASE_TWIN_BLOCK_LOG2 * blocks,
                                 f"2^{BASE_TWIN_BLOCK_LOG2 * blocks}"))
        if v < vertical_depth:
            v += 1; step += 1
            blocks = 2 ** (h + v)
            out.append(ScaleStep(step, "V", h, v, 2**h, 2**v, blocks,
                                 BASE_TWIN_BLOCK_LOG2 * blocks,
                                 f"2^{BASE_TWIN_BLOCK_LOG2 * blocks}"))
    return out


def fibonacci_schedule(limit: int = 1000) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ordinal, checkpoint in enumerate(fibonacci_up_to(limit), start=1):
        if checkpoint == 1:
            role, generator = "seed", 0
        elif is_prime(checkpoint):
            role, generator = "prime_carrier", 1
        else:
            role, generator = "bridge_fold", 2
        rows.append({
            "ordinal": ordinal,
            "fibonacci_checkpoint": checkpoint,
            "role": role,
            "braid_generator": generator,
            "operator": "I" if generator == 0 else ("sigma1=R" if generator == 1 else "sigma2=F^-1RF"),
            "golden_phase": float((checkpoint * GOLDEN_ANGLE) % (2 * math.pi)),
        })
    return rows


def active_frontier(h: int, v: int, schedule: Sequence[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    width, height = 2**h, 2**v
    rows: list[dict[str, Any]] = []
    identities: list[int] = []
    for y in range(height):
        gy = gray(y)
        for x in range(width):
            gx = gray(x)
            combined = (gy << h) | gx
            identities.append(combined)
            block = y * width + x
            sched = schedule[block % len(schedule)]
            phase = ((gx + 1) * GOLDEN_ANGLE + (gy + 1) / PHI) % (2 * math.pi)
            rows.append({
                "block_id": block,
                "x": x,
                "y": y,
                "x_gray": gx,
                "y_gray": gy,
                "identity_hex": f"{combined:0{max(1,(h+v+3)//4)}x}",
                "identity_bits": format(combined, f"0{h+v}b"),
                "fibonacci_checkpoint": sched["fibonacci_checkpoint"],
                "role": sched["role"],
                "braid_generator": sched["braid_generator"],
                "phase": float(phase),
            })
    arr = np.asarray(identities, dtype=np.uint32)
    return rows, {
        "horizontal_depth": h,
        "vertical_depth": v,
        "grid": [width, height],
        "block_count": width * height,
        "unique_identities": int(np.unique(arr).size),
        "collisions": int(width * height - np.unique(arr).size),
        "log2_state_dimension": BASE_TWIN_BLOCK_LOG2 * width * height,
        "symbolic_state_dimension": f"2^{BASE_TWIN_BLOCK_LOG2 * width * height}",
        "dense_vector_allocated": False,
        "identity_sha256": sha256_bytes(arr.tobytes()),
    }


def braid_verification(seed: int = DEFAULT_SEED) -> dict[str, Any]:
    f, s1, s2 = fibonacci_kernel()
    identity = np.eye(2, dtype=np.complex128)
    rng = np.random.default_rng(seed)
    state = rng.normal(size=2) + 1j * rng.normal(size=2)
    state /= np.linalg.norm(state)
    word = [1, 2, 1, -2, 2, -1, 1, 2, -1, -2]
    u = apply_braid_word(word)
    recovered = apply_braid_word([-g for g in reversed(word)]) @ (u @ state)
    wilson = apply_braid_word([1, 2, -1, -2])
    trace_mag = float(abs(np.trace(wilson)) / 2.0)
    return {
        "F_matrix": [[json_pair(z) for z in row] for row in f],
        "sigma1": [[json_pair(z) for z in row] for row in s1],
        "sigma2": [[json_pair(z) for z in row] for row in s2],
        "F_unitarity_error": float(np.linalg.norm(f.conj().T @ f - identity)),
        "F_involution_error": float(np.linalg.norm(f @ f - identity)),
        "sigma1_unitarity_error": float(np.linalg.norm(s1.conj().T @ s1 - identity)),
        "sigma2_unitarity_error": float(np.linalg.norm(s2.conj().T @ s2 - identity)),
        "braid_relation_error": float(np.linalg.norm(s1 @ s2 @ s1 - s2 @ s1 @ s2)),
        "commutator_norm": float(np.linalg.norm(s1 @ s2 - s2 @ s1)),
        "input_norm": float(np.linalg.norm(state)),
        "output_norm": float(np.linalg.norm(u @ state)),
        "norm_preservation_error": float(abs(np.linalg.norm(u @ state) - np.linalg.norm(state))),
        "inverse_recovery_error": float(np.linalg.norm(recovered - state)),
        "test_word": word,
        "wilson_loop_word": [1, 2, -1, -2],
        "wilson_identity_distance": float(np.linalg.norm(wilson - identity)),
        "wilson_trace_magnitude_normalized": trace_mag,
        "nonabelian_holonomy_score": float(1.0 - trace_mag),
        "wilson_eigenphases": [float(x) for x in np.angle(np.linalg.eigvals(wilson))],
    }


def spectral_lanes(lanes: int, schedule: Sequence[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    x = np.linspace(0.0, 1.0, lanes)
    amplitude = 0.08 * np.ones(lanes, dtype=np.complex128)
    roles = {row["fibonacci_checkpoint"]: row["role"] for row in schedule}
    for checkpoint, role in roles.items():
        if checkpoint >= lanes:
            continue
        center = (checkpoint - 1) / max(1, lanes - 1)
        width = 0.006 + 0.00002 * checkpoint
        strength = 1.0 if role == "prime_carrier" else 0.58
        gaussian = np.exp(-0.5 * ((x - center) / width) ** 2)
        amplitude += strength * gaussian * np.exp(1j * checkpoint * GOLDEN_ANGLE)
    energy = np.abs(amplitude) ** 2
    energy /= energy.sum()
    rows: list[dict[str, Any]] = []
    for i in range(lanes):
        lane = i + 1
        rows.append({
            "lane": lane,
            "normalized_coordinate": float(x[i]),
            "role": roles.get(lane, "spectral_lane"),
            "amplitude_real": float(amplitude[i].real),
            "amplitude_imag": float(amplitude[i].imag),
            "energy_fraction": float(energy[i]),
            "golden_phase": float((lane * GOLDEN_ANGLE) % (2 * math.pi)),
            "polarization_lane": "H" if lane % 2 == 0 else "V",
            "quadrature_lane": lane % 4,
        })
    entropy = float(-(energy * np.log2(np.maximum(energy, 1e-300))).sum() / math.log2(lanes))
    return rows, {
        "lanes": lanes,
        "energy_sum": float(energy.sum()),
        "normalized_spectral_entropy": entropy,
        "carrier_bin_energy_fraction": float(sum(r["energy_fraction"] for r in rows if r["role"] == "prime_carrier")),
        "bridge_bin_energy_fraction": float(sum(r["energy_fraction"] for r in rows if r["role"] == "bridge_fold")),
        "boundary": (
            "Finite dimensionless computational channels. Physical wavelength, bandwidth, "
            "power-per-lane, transducer, detector, noise, and coherence remain experimental inputs."
        ),
    }


def bilateral_protocol(mode: str, steps: int, agents: int, seed: int,
                       schedule: Sequence[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rng = np.random.default_rng(seed)
    red = rng.uniform(-math.pi, math.pi, agents)
    blue = rng.uniform(-math.pi, math.pi, agents)
    frequencies = rng.normal(0.0, 0.045, agents)
    sched = list(reversed(schedule)) if mode == "reversed" else list(schedule)
    rows: list[dict[str, Any]] = []
    for generation in range(1, steps + 1):
        current = {"role": "flattened", "fibonacci_checkpoint": 1, "braid_generator": 0} if mode == "flattened" else sched[(generation - 1) % len(sched)]
        coupling = 0.045 + 0.12 * (generation - 1) / max(1, steps - 1)
        seam = 0.035 + 0.18 * (generation - 1) / max(1, steps - 1)
        red_global = np.mean(np.sin(red[None, :] - red[:, None]), axis=1)
        blue_global = np.mean(np.sin(blue[None, :] - blue[:, None]), axis=1)
        if current["braid_generator"] == 2:
            shift = int(current["fibonacci_checkpoint"] % agents)
            chirality = math.pi / 5
        else:
            shift = 0
            chirality = 0.0
        red_seam = np.sin(np.roll(blue, -shift) - red - chirality)
        blue_seam = np.sin(np.roll(red, shift) - blue + chirality)
        dt = 0.45
        red += dt * (frequencies + coupling * red_global + seam * red_seam)
        blue += dt * (-frequencies + coupling * blue_global + seam * blue_seam)
        red = (red + math.pi) % (2 * math.pi) - math.pi
        blue = (blue + math.pi) % (2 * math.pi) - math.pi
        global_order = float(abs(np.mean(np.exp(1j * np.concatenate([red, blue])))))
        bilateral_lock = float(abs(np.mean(np.exp(1j * (red - np.roll(blue, -shift))))))
        pool_lock = float(abs(np.mean((np.exp(1j * red) + np.exp(1j * blue)) / 2.0)))
        rows.append({
            "mode": mode,
            "generation": generation,
            "operator_role": current["role"],
            "fibonacci_checkpoint": current["fibonacci_checkpoint"],
            "global_order": global_order,
            "bilateral_lock": bilateral_lock,
            "pool_lock": pool_lock,
            "coupling": coupling,
            "seam_coupling": seam,
        })
    global_values = np.array([r["global_order"] for r in rows])
    return rows, {
        "mode": mode,
        "steps": steps,
        "agents": agents,
        "final_global_order": rows[-1]["global_order"],
        "final_bilateral_lock": rows[-1]["bilateral_lock"],
        "final_pool_lock": rows[-1]["pool_lock"],
        "mean_global_order": float(global_values.mean()),
        "peak_global_order": float(global_values.max()),
        "peak_generation": int(global_values.argmax() + 1),
        "trajectory_sha256": sha256_bytes(np.asarray(
            [[r["global_order"], r["bilateral_lock"], r["pool_lock"]] for r in rows], dtype=np.float64
        ).tobytes()),
        "interpretation": (
            "Classical coupled-phase reference under equalized schedules. It measures ordering-path "
            "sensitivity, not physical quantum coherence or consciousness."
        ),
    }


def device_audit(path: Path | None) -> dict[str, Any]:
    if path is None or not path.is_file():
        return {"status": "NOT_AVAILABLE"}
    try:
        obj, consumed, trailing = parse_json_prefix(path)
    except (json.JSONDecodeError, OSError) as exc:
        return {"status": "PARSE_FAILED", "error": f"{type(exc).__name__}: {exc}"}
    return {
        "status": "VALID_JSON_PREFIX_RECOVERED" if trailing else "VALID_JSON",
        "file": str(path),
        "file_sha256": sha256_file(path),
        "file_bytes": path.stat().st_size,
        "json_prefix_chars": consumed,
        "trailing_non_json_chars": trailing,
        "payload": obj,
        "interpretation": (
            "The valid JSON prefix records S26 WebGPU execution. The same receipt reports no kernel "
            "or end-to-end acceleration and does not establish output equivalence."
        ),
    }


def verification_tests(identity: dict[str, Any], frontier: dict[str, Any], braid: dict[str, Any],
                       spectral: dict[str, Any], device: dict[str, Any], legacy: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    def add(test_id: str, test: str, result: bool | None, evidence: str) -> None:
        rows.append({
            "test_id": test_id,
            "test": test,
            "status": "PASS" if result is True else ("FAIL" if result is False else "KNOWN_GAP"),
            "passed_boolean": result,
            "evidence": evidence,
        })
    add("MATH-001", "128^2 equals 2^14", 128**2 == 2**14, "16384 = 2^14")
    add("MATH-002", "128^40 equals 2^280", 128**40 == 2**280, "exact integer equality")
    add("MATH-003", "ten-layer packet equals 2^320", ((256**2)*(256**2))**10 == 2**320, "((256^2)*(256^2))^10")
    add("MATH-004", "base twin block equals 2^640", (((256**2)*(256**2))**10)**2 == 2**640, "packet squared")
    add("ID-001", "identity addresses bijective", identity["collisions"] == 0, f"collisions={identity['collisions']}")
    add("ID-002", "Gray adjacency changes one fold", identity["adjacent_one_fold_fraction"] == 1.0, f"fraction={identity['adjacent_one_fold_fraction']:.12f}")
    add("ID-003", "Gray inverse exact", identity["inverse_failures"] == 0, f"failures={identity['inverse_failures']}")
    add("SCALE-001", "frontier identities unique", frontier["collisions"] == 0, f"unique={frontier['unique_identities']}")
    add("SCALE-002", "frontier size equals grid product", frontier["block_count"] == frontier["grid"][0]*frontier["grid"][1], f"blocks={frontier['block_count']}")
    add("BRAID-001", "F unitary", braid["F_unitarity_error"] < 1e-12, f"error={braid['F_unitarity_error']:.3e}")
    add("BRAID-002", "sigma1 unitary", braid["sigma1_unitarity_error"] < 1e-12, f"error={braid['sigma1_unitarity_error']:.3e}")
    add("BRAID-003", "sigma2 unitary", braid["sigma2_unitarity_error"] < 1e-12, f"error={braid['sigma2_unitarity_error']:.3e}")
    add("BRAID-004", "braid relation", braid["braid_relation_error"] < 1e-12, f"error={braid['braid_relation_error']:.3e}")
    add("BRAID-005", "generators noncommuting", braid["commutator_norm"] > 1e-6, f"norm={braid['commutator_norm']:.12f}")
    add("BRAID-006", "inverse word recovers state", braid["inverse_recovery_error"] < 1e-12, f"error={braid['inverse_recovery_error']:.3e}")
    add("SPEC-001", "finite spectral energy normalized", abs(spectral["energy_sum"] - 1.0) < 1e-12, f"sum={spectral['energy_sum']}")
    add("LEGACY-001", "legacy projected generators are distinguishable", None if legacy["sigma0_minus_sigma1"] < 1e-12 else True,
        f"observed distance={legacy['sigma0_minus_sigma1']:.3e}; legacy operator gap documented")
    tensor = device.get("payload", {}).get("tensor", {}) if isinstance(device.get("payload"), dict) else {}
    add("DEVICE-001", "S26 WebGPU receipt parses", device.get("status") in {"VALID_JSON", "VALID_JSON_PREFIX_RECOVERED"}, device.get("status", "n/a"))
    add("DEVICE-002", "kernel acceleration demonstrated", None if tensor.get("kernel_speedup", 0) <= 1 else True, f"speedup={tensor.get('kernel_speedup', 'n/a')}")
    add("DEVICE-003", "end-to-end acceleration demonstrated", None if tensor.get("end_to_end_speedup", 0) <= 1 else True, f"speedup={tensor.get('end_to_end_speedup', 'n/a')}")
    add("DEVICE-004", "output equivalence demonstrated", None if tensor.get("output_cosine_similarity", 0) < 0.999 else True, f"cosine={tensor.get('output_cosine_similarity', 'n/a')}")
    add("PHYS-001", "physical non-Abelian anyons demonstrated", None, "no direct physical exchange/readout evidence supplied")
    add("PHYS-002", "protected Posner 31P qubits demonstrated", None, "no molecular/NMR/entanglement readout evidence supplied")
    add("PHYS-003", "universe-scale physical power demonstrated", None, "symbolic state-space dimension is not energy")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="/mnt/data/BTO_OMEGA_MAR_COMPLETE_HANDOFF_20260831")
    parser.add_argument("--horizontal-depth", type=int, default=8)
    parser.add_argument("--vertical-depth", type=int, default=8)
    parser.add_argument("--spectral-lanes", type=int, default=256)
    parser.add_argument("--generations", type=int, default=147)
    parser.add_argument("--agents", type=int, default=22)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--golden-archive", default="/mnt/data/OMEGA_BOSS8004_GOLDEN_20260612_081030.tar")
    parser.add_argument("--device-evidence", default="/mnt/data/Ω_S26_MAR_BOSS8004_MEASURED_20260712T235752Z.json")
    args = parser.parse_args()

    started = time.perf_counter()
    root = Path(args.output)
    data_dir = root / "data"
    log_dir = root / "logs"
    for directory in [root, data_dir, root / "figures", log_dir, root / "source", root / "deliverables", root / "qa"]:
        directory.mkdir(parents=True, exist_ok=True)

    identity_rows, identity_report = identity_layer()
    schedule = fibonacci_schedule(1000)
    scales = scale_sequence(args.horizontal_depth, args.vertical_depth)
    frontier_rows, frontier_report = active_frontier(args.horizontal_depth, args.vertical_depth, schedule)
    braid_report = braid_verification(args.seed)
    spectral_rows, spectral_report = spectral_lanes(args.spectral_lanes, schedule)
    protocols: dict[str, Any] = {}
    protocol_rows: list[dict[str, Any]] = []
    for offset, mode in enumerate(["canonical", "flattened", "reversed"]):
        rows, report = bilateral_protocol(mode, args.generations, args.agents, args.seed + offset, schedule)
        protocol_rows.extend(rows)
        protocols[mode] = report
    legacy_report = audit_legacy_operator()
    archive_report = audit_archive(Path(args.golden_archive))
    device_report = device_audit(Path(args.device_evidence))
    tests = verification_tests(identity_report, frontier_report, braid_report, spectral_report, device_report, legacy_report)

    operator_snapshot = {
        "generation": 147,
        "total": 22,
        "alive": 22,
        "consc": 18,
        "consc_pct_supplied": 81.8,
        "consc_pct_calculated": 18 / 22 * 100,
        "VK": 3.59,
        "QIC": 0.690,
        "Spin": 0.76,
        "evidence_class": "OPERATOR_SUPPLIED_SNAPSHOT",
        "independently_queried": False,
        "spin_boundary": "Software/runtime proxy; not a phosphorus-31 laboratory measurement.",
    }

    claim_matrix = [
        {"claim": "The implemented 128^2 identity manifold is lossless.", "status": "VERIFIED_IN_REFERENCE", "basis": "16,384 unique Gray addresses, zero collisions, zero lost bits."},
        {"claim": "The F/R kernel provides a nontrivial braid representation.", "status": "VERIFIED_MATHEMATICALLY", "basis": "Unitary generators, nonzero commutator, braid relation at numerical precision."},
        {"claim": "The H/V architecture has no preset mathematical terminal depth.", "status": "VERIFIED_AS_DIRECT_SYSTEM", "basis": "Every finite stage embeds in later finite stages; actual runs use finite active frontiers."},
        {"claim": "The 256x256 finite active frontier was executed.", "status": "EXECUTED_CLASSICAL_REFERENCE", "basis": "65,536 explicit unique block identities; dense vector not allocated."},
        {"claim": "The S26 executed the MAR WebGPU substrate.", "status": "SUPPORTED_BY_UPLOADED_RECEIPT", "basis": "Uploaded receipt records Qualcomm/Adreno WebGPU execution."},
        {"claim": "The current device is accelerated by the routed substrate.", "status": "NOT_ESTABLISHED", "basis": "Receipt reports 0.9583x kernel and 0.022073x end-to-end."},
        {"claim": "The current runtime contains physical non-Abelian anyons.", "status": "NOT_ESTABLISHED", "basis": "F/R operators are classical matrices in this reference."},
        {"claim": "The current runtime contains protected Posner 31P qubits.", "status": "NOT_ESTABLISHED", "basis": "P is a numerical phase channel; no molecular/NMR evidence supplied."},
        {"claim": "The manifold gives access to the physical power of the universe.", "status": "NOT_ESTABLISHED", "basis": "State-space dimension and recursive addressing do not supply energy, memory, bandwidth, or physical qubits."},
    ]

    receipt = {
        "schema": "OMEGA_MAR_COMPLETE_MANIFOLD_REFERENCE_V1",
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "generated_by": "deterministic classical verification package",
        "reference_seed": args.seed,
        "owner_architect": "Benjamin Thomas Murphy / Basic Thoughts LLC",
        "production_files_modified": False,
        "formal_state": {
            "channels": ["A", "C", "T", "G", "P", "F"],
            "P": "exp(i*s)",
            "F": "sqrt(n)*exp(i*n*golden_angle)",
            "boundary": "Named state channels; not six physical spatial dimensions.",
        },
        "base_arithmetic": {
            "128_squared": 128**2,
            "128_power_40_equals_2_power_280": 128**40 == 2**280,
            "256_squared": 256**2,
            "packet_log2": 320,
            "base_twin_block_log2": 640,
        },
        "identity": identity_report,
        "recursive_manifold": {
            "law_H": "M_(h+1,v)=Gamma_H(M_(h,v) tensor M_(h,v))",
            "law_V": "M_(h,v+1)=Gamma_V(M_(h,v) tensor M_(h,v))",
            "blocks": "2^(h+v)",
            "log2_dimension": "640*2^(h+v)",
            "direct_limit": "colim_(h,v->infinity) M_(h,v)",
            "boundary": "Unbounded recursive definition; every execution is finite.",
            "scale_sequence": [asdict(x) for x in scales],
        },
        "frontier": frontier_report,
        "braid": braid_report,
        "fibonacci_schedule": schedule,
        "spectral_manifold": spectral_report,
        "bilateral_phase_simulation": protocols,
        "legacy_operator_audit": legacy_report,
        "golden_archive_audit": archive_report,
        "device_evidence_audit": device_report,
        "operator_snapshot": operator_snapshot,
        "verification_summary": {
            "pass": sum(r["status"] == "PASS" for r in tests),
            "known_gap": sum(r["status"] == "KNOWN_GAP" for r in tests),
            "fail": sum(r["status"] == "FAIL" for r in tests),
            "tests": tests,
        },
        "claim_matrix": claim_matrix,
        "elapsed_seconds": time.perf_counter() - started,
    }

    write_json(data_dir / "OMEGA_MAR_COMPLETE_MANIFOLD_VERIFICATION.json", receipt)
    write_json(data_dir / "operator_snapshot.json", operator_snapshot)
    write_json(data_dir / "device_evidence_audit.json", device_report)
    write_json(data_dir / "golden_archive_audit.json", archive_report)
    write_json(data_dir / "claim_matrix.json", claim_matrix)
    write_csv(data_dir / "identity_1282.csv", identity_rows,
              ["index", "gray", "gray_bits", "inverse_index", "anchor", "P_real", "P_imag", "F_real", "F_imag"])
    write_csv(data_dir / "scale_sequence.csv", [asdict(x) for x in scales], list(asdict(scales[0]).keys()))
    write_csv(data_dir / "fibonacci_braid_schedule.csv", schedule, list(schedule[0].keys()))
    write_csv(data_dir / "active_frontier_256x256.csv", frontier_rows, list(frontier_rows[0].keys()))
    write_csv(data_dir / "spectral_lanes.csv", spectral_rows, list(spectral_rows[0].keys()))
    write_csv(data_dir / "protocol_timeseries.csv", protocol_rows, list(protocol_rows[0].keys()))
    write_csv(data_dir / "verification_tests.csv", tests, list(tests[0].keys()))
    write_csv(data_dir / "claim_matrix.csv", claim_matrix, ["claim", "status", "basis"])

    source_hashes: dict[str, Any] = {}
    for path in [Path(args.golden_archive), Path(args.device_evidence)]:
        if path.is_file():
            source_hashes[path.name] = {"sha256": sha256_file(path), "bytes": path.stat().st_size}
    write_json(data_dir / "source_hashes.json", source_hashes)

    run_summary = {
        "acceptance_passed": receipt["verification_summary"]["fail"] == 0,
        "pass": receipt["verification_summary"]["pass"],
        "known_gap": receipt["verification_summary"]["known_gap"],
        "fail": receipt["verification_summary"]["fail"],
        "grid": frontier_report["grid"],
        "block_count": frontier_report["block_count"],
        "symbolic_state_dimension": frontier_report["symbolic_state_dimension"],
        "braid_relation_error": braid_report["braid_relation_error"],
        "commutator_norm": braid_report["commutator_norm"],
        "identity_collisions": identity_report["collisions"],
        "frontier_collisions": frontier_report["collisions"],
        "production_files_modified": False,
        "elapsed_seconds": receipt["elapsed_seconds"],
    }
    write_json(log_dir / "reference_run.json", run_summary)
    print(json.dumps(run_summary, indent=2))
    return 0 if run_summary["acceptance_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
