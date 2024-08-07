//
//  ViewController.swift
//  TinyVPN
//
//  Created by Burkan Yılmaz on 7.08.2024.
//

import Factory
import UIKit

class ViewController: UIViewController {

    @LazyInjected(\.vpnConnectionService) var vpnService

    var connectButton: UIButton!
    
    var selected: VPN!
    var status: Bool = false {
        didSet {
            if status {
                connectButton.setTitle("Connect", for: .normal)
            } else {
                connectButton.setTitle("Disconnect", for: .normal)
            }
        }
    }
    
    override func loadView() {
        super.loadView()
        connectButton = UIButton(type: .system)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setup()
    }
    
    private func setup() {
        selected = VPN(ip: "", psk: "", password: "", username: "")
        
        view.backgroundColor = .systemBackground
        
        view.addSubview(connectButton)
        connectButton.setTitle("Connect", for: .normal)
        connectButton.translatesAutoresizingMaskIntoConstraints = false
        connectButton.centerYAnchor.constraint(equalTo: view.centerYAnchor).isActive = true
        connectButton.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: Magics.standartInsets.left).isActive = true
        connectButton.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: Magics.standartInsets.right).isActive = true
        connectButton.heightAnchor.constraint(equalToConstant: Magics.standartButtonHeight).isActive = true
        connectButton.addTarget(self, action: #selector(tap), for: .touchUpInside)
    }
    
    @objc
    private func tap() {
        if status {
            vpnService.stopVPN()
        } else {
            vpnService.startVPN(vpnModel: selected) { [weak self] (error) in
                guard let self = self else { return }
                if error == nil {
                    self.status = true
                    print("Connected")
                } else {
                    self.status = false
                    print("NOT Connected - \(error!.localizedDescription)")
                }
            }
        }
    }

}

