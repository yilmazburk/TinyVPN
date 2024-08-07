//
//  VPNManager.swift
//  TinyVPN
//
//  Created by Burkan Yılmaz on 7.08.2024.
//

import Foundation
import SwiftKeychainWrapper
import NetworkExtension

typealias Completion = (Error?) -> Void

protocol VPNService: AnyObject {
    func startVPN(vpnModel: VPN, completion: @escaping Completion)
    func stopVPN()
}

final class VPNConnectionManager: VPNService {
    func startVPN(vpnModel: VPN, completion: @escaping Completion) {
        NEVPNManager.shared().loadFromPreferences { (error) in
            guard error == nil else { 
                completion(error!)
                return
            }
            
            KeychainWrapper.standard.set(vpnModel.psk, forKey: "psk")
            KeychainWrapper.standard.set(vpnModel.password, forKey: "pass")

            let ipSecProtocol = NEVPNProtocolIPSec()
            ipSecProtocol.serverAddress = vpnModel.ip
            ipSecProtocol.remoteIdentifier = vpnModel.ip
            ipSecProtocol.authenticationMethod = .sharedSecret
            ipSecProtocol.sharedSecretReference = KeychainWrapper.standard.dataRef(forKey: "psk")
            ipSecProtocol.passwordReference = KeychainWrapper.standard.dataRef(forKey: "pass")
            ipSecProtocol.username = vpnModel.username
            
            NEVPNManager.shared().onDemandRules = [NEOnDemandRuleConnect()]
            NEVPNManager.shared().isOnDemandEnabled = false
            
            NEVPNManager.shared().protocolConfiguration = ipSecProtocol
            NEVPNManager.shared().localizedDescription = Magics.localiedDescription
            
            NEVPNManager.shared().saveToPreferences(completionHandler: { (error) in
                guard error == nil else { completion(error!); return }
                
                NEVPNManager.shared().loadFromPreferences { (error) in
                    guard error == nil else { completion(error!); return }
                    
                    NEVPNManager.shared().isEnabled = true
                    
                    NEVPNManager.shared().saveToPreferences(completionHandler: { (err) in
                        guard err == nil else { completion(err!); return }
                        
                        do {
                            try NEVPNManager.shared().connection.startVPNTunnel()
                            DispatchQueue.main.async {
                                completion(nil)
                            }
                        }  catch {
                            DispatchQueue.main.async {
                                completion(error)
                            }
                        }
                    })
                }
            })
        }
    }
    
    func stopVPN() {
        NEVPNManager.shared().connection.stopVPNTunnel()
    }
}
