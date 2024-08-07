//
//  Container+Extension.swift
//  TinyVPN
//
//  Created by Burkan Yılmaz on 7.08.2024.
//

import Factory
import Foundation

extension Container {
    var vpnConnectionService: Factory<VPNService> {
        self { VPNConnectionManager() }
            .singleton
    }
}
