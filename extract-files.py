#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

blob_fixups: blob_fixups_user_type = {
    'vendor/etc/init/init.batterysecret.rc': blob_fixup()
        .regex_replace('.*seclabel u:r:batterysecret:s0\n', ''),
    'vendor/etc/sensors/hals.conf': blob_fixup()
        .add_line_if_missing('sensors.udfps.so'),
    'vendor/lib/hw/audio.primary.raphael.so': blob_fixup()
        .binary_regex_replace(
            b'/vendor/lib/liba2dpoffload.so',
            b'liba2dpoffload_raphael.so\x00\x00\x00\x00',
        )
        .replace_needed('libaudioroute.so', 'libaudioroute-v34.so'),
    'vendor/lib/libaudioroute_ext.so': blob_fixup()
        .replace_needed('libaudioroute.so', 'libaudioroute-v34.so'),
    'vendor/lib64/camera/components/com.qti.node.watermark.so': blob_fixup()
        .add_needed('libpiex_shim.so'),
    (
        'vendor/lib64/libalLDC.so',
        'vendor/lib64/libalAILDC.so',
        'vendor/lib64/libalhLDC.so',
    ): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
    (
        'vendor/lib64/libarcsoft_dualcam_refocus_front.so',
        'vendor/lib64/libarcsoft_dualcam_refocus_rear_t.so',
        'vendor/lib64/libarcsoft_dualcam_refocus_rear_w.so',
    ): blob_fixup()
        .clear_symbol_version('remote_handle_close')
        .clear_symbol_version('remote_handle_invoke')
        .clear_symbol_version('remote_handle_open'),
    'vendor/lib64/libhvx_proxy_stub.so': blob_fixup()
        .clear_symbol_version('remote_handle64_close')
        .clear_symbol_version('remote_handle64_invoke')
        .clear_symbol_version('remote_handle64_open')
        .clear_symbol_version('remote_register_dma_handle')
        .clear_symbol_version('remote_register_dma_handle_attr'),
}  # fmt: skip

namespace_imports = [
    'hardware/qcom-caf/common/libqti-perfd-client',
    'hardware/qcom-caf/sm8150',
    'hardware/xiaomi',
    'vendor/qcom/opensource/display',
    'vendor/xiaomi/sm8150-common',
]

module = ExtractUtilsModule(
    'raphael',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(
        module, 'sm8150-common', module.vendor
    )
    utils.run()
