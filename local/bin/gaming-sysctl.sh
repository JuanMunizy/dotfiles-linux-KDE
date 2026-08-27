#!/bin/bash
# ========================================
# Aplicar Otimizações de Kernel para Gaming
# Execute com: sudo bash ~/.local/bin/gaming-sysctl.sh
# ========================================

cat > /etc/sysctl.d/99-gaming.conf << 'EOF'
# Sysctl Otimizações para Gaming - Ryzen 5 5600GT + RX 7600
vm.swappiness = 10
vm.dirty_background_ratio = 5
vm.dirty_ratio = 15
vm.vfs_cache_pressure = 50
kernel.nmi_watchdog = 0
vm.dirty_expire_centisecs = 3000
vm.dirty_writeback_centisecs = 500
kernel.perf_event_paranoid = -1
kernel.kptr_restrict = 0
EOF

sysctl --system 2>/dev/null
echo "Sysctl gaming optimizations applied!"
