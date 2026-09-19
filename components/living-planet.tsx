"use client";

import { Canvas, useFrame } from "@react-three/fiber";
import { Float, Sparkles } from "@react-three/drei";
import { useMemo, useRef } from "react";
import * as THREE from "three";

function Planet() {
  const group = useRef<THREE.Group>(null);
  const shell = useRef<THREE.Mesh>(null);
  const points = useMemo(() => {
    const vertices = new Float32Array(1800 * 3);
    for (let i = 0; i < vertices.length; i += 3) {
      const radius = 2.25 + Math.random() * 0.7;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      vertices[i] = radius * Math.sin(phi) * Math.cos(theta);
      vertices[i + 1] = radius * Math.cos(phi);
      vertices[i + 2] = radius * Math.sin(phi) * Math.sin(theta);
    }
    return vertices;
  }, []);
  useFrame(({ clock, pointer }, delta) => {
    if (!group.current || !shell.current) return;
    group.current.rotation.y += delta * 0.035;
    group.current.rotation.x = THREE.MathUtils.lerp(group.current.rotation.x, pointer.y * 0.08, 0.02);
    group.current.rotation.z = THREE.MathUtils.lerp(group.current.rotation.z, -pointer.x * 0.08, 0.02);
    const pulse = 1 + Math.sin(clock.elapsedTime * 0.45) * 0.018;
    shell.current.scale.setScalar(pulse);
  });
  return (
    <group ref={group}>
      <mesh ref={shell}>
        <sphereGeometry args={[2.2, 96, 96]} />
        <meshPhysicalMaterial color="#170305" roughness={0.54} metalness={0.28} clearcoat={0.7} clearcoatRoughness={0.3} />
      </mesh>
      <mesh rotation={[0.4, 0.2, -0.15]}>
        <torusGeometry args={[2.65, 0.015, 8, 240]} />
        <meshBasicMaterial color="#cf2e36" transparent opacity={0.55} />
      </mesh>
      <points>
        <bufferGeometry><bufferAttribute attach="attributes-position" args={[points, 3]} /></bufferGeometry>
        <pointsMaterial color="#eb4d52" size={0.012} transparent opacity={0.55} depthWrite={false} />
      </points>
      <Sparkles count={90} scale={7} size={1.2} speed={0.12} color="#d3aa54" opacity={0.55} />
    </group>
  );
}

export function LivingPlanet() {
  return (
    <div className="planet" aria-hidden="true">
      <Canvas camera={{ position: [0, 0, 7], fov: 42 }} dpr={[1, 1.5]} gl={{ antialias: true, powerPreference: "high-performance", alpha: true }}>
        <ambientLight intensity={0.22} />
        <pointLight position={[-4, 2, 4]} color="#d22932" intensity={30} distance={10} />
        <pointLight position={[4, -2, 2]} color="#d3aa54" intensity={13} distance={9} />
        <Float speed={0.35} rotationIntensity={0.08} floatIntensity={0.2}><Planet /></Float>
      </Canvas>
    </div>
  );
}
